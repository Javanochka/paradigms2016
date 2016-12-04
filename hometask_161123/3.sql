select City.name
from Country, Capital, City
where Country.Name like 'Malaysia' and Country.Code = Capital.CountryCode and Capital.CityId = City.Id;
