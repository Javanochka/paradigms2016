select GovernmentForm, sum(SurfaceArea) area
from Country
group by GovernmentForm
order by area desc
limit 1;
