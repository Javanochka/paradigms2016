select Country.Name, Country.Population, Country.SurfaceArea
from Country inner join Capital on Country.Code = Capital.CountryCode inner join City on Country.Code = City.CountryCode
group by Country.Name having Capital.CityId != City.Id and City.Population = max(City.Population)
order by 1.0 * Country.Population / Country.SurfaceArea desc, Country.Name;
