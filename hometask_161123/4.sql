select Country.Name, sum(City.CountryCode = Country.Code and City.Population >= 1000000) num
from Country, City
group by Country.Name
order by num desc, Country.Name;
