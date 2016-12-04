select First.Year, Second.Year, Country.Name, 1.0 * (Second.Rate-First.Rate)/(Second.Year-First.Year) added
from Country inner join LiteracyRate First on Country.Code = First.CountryCode inner join LiteracyRate Second on Country.Code = Second.CountryCode and Second.Year > First.Year
group by Country.Name, First.Year having Second.Year = min(Second.Year)
order by added desc;
