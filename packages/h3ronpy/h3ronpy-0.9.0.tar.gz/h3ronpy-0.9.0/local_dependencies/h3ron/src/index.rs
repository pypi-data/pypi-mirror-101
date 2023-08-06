use std::convert::TryFrom;
use std::ffi::CString;
use std::mem::MaybeUninit;
use std::os::raw::c_int;
use std::str::FromStr;

use geo_types::{Coordinate, LineString, Point, Polygon};
use serde::{Deserialize, Serialize};

use h3ron_h3_sys::{GeoCoord, H3Index};

use crate::error::Error;
use crate::util::{coordinate_to_geocoord, drain_h3indexes_to_indexes, point_to_geocoord};
use crate::{max_k_ring_size, AreaUnits, FromH3Index, HasH3Index, ToCoordinate, ToPolygon};

/// a single H3 index
#[derive(PartialOrd, PartialEq, Clone, Debug, Serialize, Deserialize, Hash, Eq, Ord, Copy)]
pub struct Index(H3Index);

/*
impl From<H3Index> for Index {
    fn from(h3index: H3Index) -> Self {
        Index(h3index)
    }
}

 */

/// marker trait for indexes
pub trait ToIndex {
    fn to_index(&self) -> Index;
}

impl ToIndex for H3Index {
    fn to_index(&self) -> Index {
        Index::new(*self)
    }
}

impl ToIndex for Index {
    fn to_index(&self) -> Index {
        *self
    }
}

/// convert to index including validation
impl TryFrom<u64> for Index {
    type Error = Error;

    fn try_from(h3index: H3Index) -> Result<Self, Self::Error> {
        let index = Index::new(h3index);
        index.validate()?;
        Ok(index)
    }
}

impl HasH3Index for Index {
    fn h3index(&self) -> H3Index {
        self.0
    }
}

impl FromH3Index for Index {
    fn from_h3index(h3index: H3Index) -> Self {
        Index::new(h3index)
    }
}

impl Index {
    /// create an index from the given u64.
    ///
    /// No validation is performed - use the `TryInto` trait in
    /// case that is desired.
    pub fn new(h3index: H3Index) -> Self {
        Self(h3index)
    }

    pub fn resolution(&self) -> u8 {
        (unsafe { h3ron_h3_sys::h3GetResolution(self.0) }) as u8
    }

    /// Checks the validity of the index
    pub fn is_valid(&self) -> bool {
        unsafe { h3ron_h3_sys::h3IsValid(self.0) != 0 }
    }

    /// Checks the validity of the index
    pub fn validate(&self) -> Result<(), Error> {
        if !self.is_valid() {
            Err(Error::InvalidH3Index)
        } else {
            Ok(())
        }
    }

    pub fn is_parent_of(&self, other: &Index) -> bool {
        *self == other.get_parent_unchecked(self.resolution())
    }

    pub fn is_child_of(&self, other: &Index) -> bool {
        other.is_parent_of(self)
    }

    pub fn contains(&self, other: &Index) -> bool {
        self.is_parent_of(other)
    }

    /// Retrieves the parent index at `parent_resolution`.
    ///
    /// # Returns
    ///
    /// This method may fail if the `parent_resolution` is higher than current `self` resolution.
    ///
    /// If you don't want it to fail use `get_parent_unchecked`
    pub fn get_parent(&self, parent_resolution: u8) -> Result<Self, Error> {
        let res = self.get_parent_unchecked(parent_resolution);
        res.validate()?;
        Ok(res)
    }

    /// Retrieves the parent index at `parent_resolution`.
    ///
    /// # Returns
    ///
    /// This method may return an invalid `Index` if the `parent_resolution`is higher than current
    /// `self` resolution.
    ///
    /// Use `get_parent` for validity check.
    pub fn get_parent_unchecked(&self, parent_resolution: u8) -> Self {
        Index::new(unsafe { h3ron_h3_sys::h3ToParent(self.0, parent_resolution as c_int) })
    }

    pub fn get_children(&self, child_resolution: u8) -> Vec<Self> {
        let max_size =
            unsafe { h3ron_h3_sys::maxH3ToChildrenSize(self.0, child_resolution as c_int) };
        let mut h3_indexes_out: Vec<h3ron_h3_sys::H3Index> = vec![0; max_size as usize];
        unsafe {
            h3ron_h3_sys::h3ToChildren(
                self.0,
                child_resolution as c_int,
                h3_indexes_out.as_mut_ptr(),
            );
        }
        drain_h3indexes_to_indexes(h3_indexes_out)
    }

    /// Build a new `Index` from a `Point`.
    ///
    /// # Returns
    /// The built index may be invalid.
    /// Use the `from_point` method for validity check.
    pub fn from_point_unchecked(pt: &Point<f64>, h3_resolution: u8) -> Self {
        let h3index = unsafe {
            let gc = point_to_geocoord(pt);
            h3ron_h3_sys::geoToH3(&gc, h3_resolution as c_int)
        };
        Index::new(h3index)
    }

    /// Build a new `Index` from a `Point`.
    ///
    /// # Returns
    /// If the built index is invalid, returns an Error.
    /// Use the `from_point_unchecked` to avoid error.
    pub fn from_point(pt: &Point<f64>, h3_resolution: u8) -> Result<Self, Error> {
        let res = Self::from_point_unchecked(pt, h3_resolution);
        res.validate()?;
        Ok(res)
    }

    /// Build a new `Index` from coordinates.
    ///
    /// # Returns
    /// The built index may be invalid.
    /// Use the `from_coordinate` method for validity check.
    pub fn from_coordinate_unchecked(c: &Coordinate<f64>, h3_resolution: u8) -> Self {
        let h3index = unsafe {
            let gc = coordinate_to_geocoord(c);
            h3ron_h3_sys::geoToH3(&gc, h3_resolution as c_int)
        };
        Index::new(h3index)
    }

    /// Build a new `Index` from coordinates.
    ///
    /// # Returns
    /// If the built index is invalid, returns an Error.
    /// Use the `from_coordinate_unchecked` to avoid error.
    pub fn from_coordinate(c: &Coordinate<f64>, h3_resolution: u8) -> Result<Self, Error> {
        let res = Self::from_coordinate_unchecked(c, h3_resolution);
        res.validate()?;
        Ok(res)
    }

    /// Checks if the current index and `other` are neighbors.
    pub fn is_neighbor_to(&self, other: &Self) -> bool {
        let res: i32 = unsafe { h3ron_h3_sys::h3IndexesAreNeighbors(self.0, other.0) };
        res == 1
    }

    pub fn k_ring(&self, k: u32) -> Vec<Index> {
        let max_size = unsafe { h3ron_h3_sys::maxKringSize(k as i32) as usize };
        let mut h3_indexes_out: Vec<H3Index> = vec![0; max_size];

        unsafe {
            h3ron_h3_sys::kRing(self.0, k as c_int, h3_indexes_out.as_mut_ptr());
        }
        remove_zero_indexes_from_vec!(h3_indexes_out);
        drain_h3indexes_to_indexes(h3_indexes_out)
    }

    pub fn hex_ring(&self, k: u32) -> Result<Vec<Index>, Error> {
        // calculation of max_size taken from
        // https://github.com/uber/h3-py/blob/dd08189b378429291c342d0af3d3cc1e38a659d5/src/h3/_cy/cells.pyx#L111
        let max_size = if k > 0 { 6 * k as usize } else { 1 };
        let mut h3_indexes_out: Vec<H3Index> = vec![0; max_size];

        let res = unsafe {
            h3ron_h3_sys::hexRing(self.0, k as c_int, h3_indexes_out.as_mut_ptr()) as c_int
        };
        if res == 0 {
            Ok(drain_h3indexes_to_indexes(h3_indexes_out))
        } else {
            Err(Error::PentagonalDistortion)
        }
    }

    /// Retrieves indexes around `self` through K Rings.
    ///
    /// # Arguments
    ///
    /// * `k_min` - the minimum k ring distance
    /// * `k_max` - the maximum k ring distance
    ///
    /// # Returns
    ///
    /// A `Vec` of `(u32, Index)` tuple is returned. The `u32` value is the K Ring distance
    /// of the `Index` value.
    pub fn k_ring_distances(&self, k_min: u32, k_max: u32) -> Vec<(u32, Index)> {
        let max_size = max_k_ring_size(k_max);
        let mut h3_indexes_out: Vec<H3Index> = vec![0; max_size];
        let mut distances_out: Vec<c_int> = vec![0; max_size];
        unsafe {
            h3ron_h3_sys::kRingDistances(
                self.0,
                k_max as c_int,
                h3_indexes_out.as_mut_ptr(),
                distances_out.as_mut_ptr(),
            )
        };
        self.associate_index_distances(h3_indexes_out, distances_out, k_min)
    }

    pub fn hex_range_distances(&self, k_min: u32, k_max: u32) -> Result<Vec<(u32, Index)>, Error> {
        let max_size = unsafe { h3ron_h3_sys::maxKringSize(k_max as c_int) as usize };
        let mut h3_indexes_out: Vec<H3Index> = vec![0; max_size];
        let mut distances_out: Vec<c_int> = vec![0; max_size];
        let res = unsafe {
            h3ron_h3_sys::hexRangeDistances(
                self.0,
                k_max as c_int,
                h3_indexes_out.as_mut_ptr(),
                distances_out.as_mut_ptr(),
            ) as c_int
        };
        if res == 0 {
            Ok(self.associate_index_distances(h3_indexes_out, distances_out, k_min))
        } else {
            Err(Error::PentagonalDistortion) // may also be PentagonEncountered
        }
    }

    /// Retrieves the number of K Rings between `self` and `other`.
    ///
    /// For distance in miles or kilometers use haversine algorithms.
    pub fn distance_to(&self, other: &Self) -> i32 {
        unsafe { h3ron_h3_sys::h3Distance(self.0, other.0) }
    }

    fn associate_index_distances(
        &self,
        mut h3_indexes_out: Vec<H3Index>,
        distances_out: Vec<c_int>,
        k_min: u32,
    ) -> Vec<(u32, Index)> {
        h3_indexes_out
            .drain(..)
            .enumerate()
            .filter(|(idx, h3index)| *h3index != 0 && distances_out[*idx] >= k_min as i32)
            .map(|(idx, h3index)| (distances_out[idx] as u32, Index::new(h3index)))
            .collect()
    }

    /// exact area for a specific cell (hexagon or pentagon)
    pub fn area(&self, area_units: AreaUnits) -> f64 {
        match area_units {
            AreaUnits::M2 => unsafe { h3ron_h3_sys::cellAreaM2(self.0) },
            AreaUnits::Km2 => unsafe { h3ron_h3_sys::cellAreaKm2(self.0) },
            AreaUnits::Radians2 => unsafe { h3ron_h3_sys::cellAreaRads2(self.0) },
        }
    }

    /// determines if an H3 cell is a pentagon
    pub fn is_pentagon(&self) -> bool {
        unsafe { h3ron_h3_sys::h3IsPentagon(self.0) == 1 }
    }

    /// returns the base cell "number" (0 to 121) of the provided H3 cell
    pub fn get_base_cell(&self) -> u8 {
        unsafe { h3ron_h3_sys::h3GetBaseCell(self.0) as u8 }
    }
}

impl ToString for Index {
    fn to_string(&self) -> String {
        format!("{:x}", self.0)
    }
}

impl FromStr for Index {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let h3index: H3Index = CString::new(s)
            .map(|cs| unsafe { h3ron_h3_sys::stringToH3(cs.as_ptr()) })
            .map_err(|_| Error::InvalidInput)?;
        Index::try_from(h3index)
    }
}

impl ToPolygon for Index {
    /// the polygon spanning the area of the index
    fn to_polygon(&self) -> Polygon<f64> {
        let gb = unsafe {
            let mut mu = MaybeUninit::<h3ron_h3_sys::GeoBoundary>::uninit();
            h3ron_h3_sys::h3ToGeoBoundary(self.0, mu.as_mut_ptr());
            mu.assume_init()
        };

        let mut nodes = vec![];
        for i in 0..gb.numVerts {
            nodes.push((
                unsafe { h3ron_h3_sys::radsToDegs(gb.verts[i as usize].lon) },
                unsafe { h3ron_h3_sys::radsToDegs(gb.verts[i as usize].lat) },
            ));
        }
        nodes.push(*nodes.first().unwrap());
        Polygon::new(LineString::from(nodes), vec![])
    }
}

impl ToCoordinate for Index {
    /// the centroid coordinate of the h3 index
    fn to_coordinate(&self) -> Coordinate<f64> {
        unsafe {
            let mut gc = GeoCoord { lat: 0.0, lon: 0.0 };
            h3ron_h3_sys::h3ToGeo(self.0, &mut gc);

            Coordinate {
                x: h3ron_h3_sys::radsToDegs(gc.lon),
                y: h3ron_h3_sys::radsToDegs(gc.lat),
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::convert::{TryFrom, TryInto};
    use std::str::FromStr;

    use bincode::{deserialize, serialize};

    use h3ron_h3_sys::H3Index;

    use crate::index::Index;
    use crate::HasH3Index;

    #[test]
    fn test_h3_to_string() {
        let h3index = 0x89283080ddbffff_u64;
        assert_eq!(
            Index::try_from(h3index).unwrap().to_string(),
            "89283080ddbffff".to_string()
        );
    }

    #[test]
    fn test_string_to_h3() {
        let index = Index::from_str("89283080ddbffff").expect("parsing failed");
        assert_eq!(Index::try_from(0x89283080ddbffff_u64).unwrap(), index);
    }

    #[test]
    fn test_is_valid() {
        assert_eq!(
            Index::try_from(0x89283080ddbffff_u64).unwrap().is_valid(),
            true
        );
        assert_eq!(Index::new(0_u64).is_valid(), false);
        assert!(Index::try_from(0_u64).is_err());
    }

    #[test]
    fn test_hex_ring_1() {
        let idx = Index::try_from(0x89283080ddbffff_u64).unwrap();
        let ring = idx.hex_ring(1).unwrap();
        assert_eq!(ring.len(), 6);
        assert!(ring.iter().all(|index| index.is_valid()));
    }

    #[test]
    fn test_hex_ring_0() {
        let idx = Index::new(0x89283080ddbffff_u64);
        let ring = idx.hex_ring(0).unwrap();
        assert_eq!(ring.len(), 1);
        assert!(ring.iter().all(|index| index.is_valid()));
    }

    #[test]
    fn test_k_ring_distances() {
        let idx = Index::new(0x89283080ddbffff_u64);
        let k_min = 2;
        let k_max = 2;
        let indexes = idx.k_ring_distances(k_min, k_max);
        assert!(indexes.len() > 10);
        for (k, index) in indexes.iter() {
            assert!(index.is_valid());
            assert!(*k >= k_min);
            assert!(*k <= k_max);
        }
    }

    #[test]
    fn test_hex_range_distances() {
        let idx = Index::new(0x89283080ddbffff_u64);
        let k_min = 2;
        let k_max = 2;
        let indexes = idx.hex_range_distances(k_min, k_max).unwrap();
        assert!(indexes.len() > 10);
        for (k, index) in indexes.iter() {
            assert!(index.is_valid());
            assert!(*k >= k_min);
            assert!(*k <= k_max);
        }
    }

    #[test]
    fn test_hex_range_distances_2() {
        let idx = Index::new(0x89283080ddbffff_u64);
        let k_min = 0;
        let k_max = 10;
        let indexes = idx.hex_range_distances(k_min, k_max).unwrap();

        let mut indexes_resolutions: HashMap<H3Index, Vec<u32>> = HashMap::new();
        for (dist, idx) in indexes.iter() {
            indexes_resolutions
                .entry(idx.h3index())
                .and_modify(|v| v.push(*dist))
                .or_insert_with(|| vec![*dist]);
        }

        println!("{:?}", indexes_resolutions);
        assert!(indexes.len() > 10);
        for (k, index) in indexes.iter() {
            assert!(index.is_valid());
            assert!(*k >= k_min);
            assert!(*k <= k_max);
        }
    }

    #[test]
    fn serde_index_roundtrip() {
        let idx = Index::new(0x89283080ddbffff_u64);
        let serialized_data = serialize(&idx).unwrap();
        let idx_2: Index = deserialize(&serialized_data).unwrap();
        assert_eq!(idx, idx_2);
        assert_eq!(idx.h3index(), idx_2.h3index());
    }

    /// this test is not really a hard requirement, but it is nice to know
    /// Index is handled just like an u64
    #[test]
    fn serde_index_from_h3index() {
        let idx: H3Index = 0x89283080ddbffff_u64;
        let serialized_data = serialize(&idx).unwrap();
        let idx_2: Index = deserialize(&serialized_data).unwrap();
        assert_eq!(idx, idx_2.h3index());
    }

    #[test]
    fn test_is_neighbor() {
        let idx: Index = 0x89283080ddbffff_u64.try_into().unwrap();
        let ring = idx.hex_ring(1).unwrap();
        let neighbor = ring.first().unwrap();
        assert!(idx.is_neighbor_to(neighbor));
        let wrong_neighbor = 0x8a2a1072b59ffff_u64.try_into().unwrap();
        assert!(!idx.is_neighbor_to(&wrong_neighbor));
        // Self
        assert!(!idx.is_neighbor_to(&idx));
    }

    #[test]
    fn test_distance_to() {
        let idx: Index = 0x89283080ddbffff_u64.try_into().unwrap();
        assert_eq!(idx.distance_to(&idx), 0);
        let ring = idx.hex_ring(1).unwrap();
        let neighbor = ring.first().unwrap();
        assert_eq!(idx.distance_to(&neighbor), 1);
        let ring = idx.hex_ring(3).unwrap();
        let neighbor = ring.first().unwrap();
        assert_eq!(idx.distance_to(&neighbor), 3);
    }
}
