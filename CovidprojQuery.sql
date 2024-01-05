Select *
From [Covid Project]..CovidDeaths$
where continent is not null
order by 3,4
Select *
From [Covid Project]..CovidVaccinations$ 

--Select Data that we are going to use 
Select Location, date, total_cases, new_cases, total_deaths, population
From [Covid Project]..CovidDeaths$
order by 1,2

-- looking at total cases Vs total Deaths
-- show likelihood of dying if infected by covid in Thailand
Select Location,date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from [Covid Project]..CovidDeaths$
Where location like '%Thai%'
order by 1,2 

--Looking at total cases Vs poppulation of Thailand
Select location,date,population,  total_cases, (total_cases/population)*100 as CasesbyPopulation
From [Covid Project]..CovidDeaths$
Where location like '%Thai%'
order by 1,2

--look at countries with highest infected rate compared to population
Select location,MAX(total_cases),population, (Max(total_cases)/population)*100 As PercentInfectedRate
From [Covid Project]..CovidDeaths$
Group by location, population
Order by PercentInfectedRate desc

--look at new cases by date
Select location,date, new_cases
from [Covid Project]..CovidDeaths$
Where date =   '2020-09-20 00:00:00.000' 

--showing countries with highest death count per Population 
Select location, Max(cast(total_deaths as int)) as TotalDeathCount
From [Covid Project]..CovidDeaths$
where continent is not null
Group by Location
order by TotalDeathCount desc

-- showing continent that have highest death count
Select continent, Max(cast(total_deaths as int)) as TotalDeathByContinent
From [Covid Project]..CovidDeaths$
Where continent is not null
Group by continent
Order by TotalDeathByContinent desc

-- Global Numbers by each date
Select  date, sum(new_cases) as TotalNewCases , Sum(cast(new_deaths as int)) as TotalNewDeath, Sum(cast(new_deaths as int)) / sum(new_cases)*100 as
TotalDeathPercentage
FRom [Covid Project]..CovidDeaths$
where continent is not null
Group by date
order by 1,2

--Total new cases / deaths and Death percentage of global
Select  sum(new_cases) as TotalNewCases , Sum(cast(new_deaths as int)) as TotalNewDeath, Sum(cast(new_deaths as int)) / sum(new_cases)*100 as
TotalDeathPercentage
From [Covid Project]..CovidDeaths$
where continent is not null
order by 1,2

-- looking at total population vs vaccinations
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(cast(vac.new_vaccinations as int)) over (Partition by dea.location order by dea.location, dea.date)
as RollingPeopleVaccinated

from [Covid Project]..CovidDeaths$ dea
join [Covid Project]..CovidVaccinations$ vac
on dea.location = vac.location and
	dea.date = vac.date
where dea.continent is not null
order by 2,3 desc

--USE CTE

With PopvsVac (Continent, Location,Date,Population,New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(cast(vac.new_vaccinations as int)) over (Partition by dea.location order by dea.location, dea.date)
as RollingPeopleVaccinated

from [Covid Project]..CovidDeaths$ dea
join [Covid Project]..CovidVaccinations$ vac
on dea.location = vac.location and
	dea.date = vac.date
where dea.continent is not null
--order by 2,3 desc
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac

--Temp Table
Drop Table if Exists #PercenPopulationVaccinated
Create Table #PercenPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar (255),
Date datetime,
Population numeric, 
New_Vaccinated numeric,
RollingPeopleVaccinated numeric,
)

Insert Into #PercenPopulationVaccinated 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(cast(vac.new_vaccinations as int)) over (Partition by dea.location order by dea.location, dea.date)
as RollingPeopleVaccinated

from [Covid Project]..CovidDeaths$ dea
join [Covid Project]..CovidVaccinations$ vac
on dea.location = vac.location and
	dea.date = vac.date
where dea.continent is not null
--order by 2,3 desc

Select *, (RollingPeopleVaccinated / Population)*100
From #PercenPopulationVaccinated


--Creating View To store data for later visualization
Create View PercenPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
Sum(cast(vac.new_vaccinations as int)) over (Partition by dea.location order by dea.location, dea.date)
as RollingPeopleVaccinated

from [Covid Project]..CovidDeaths$ dea
join [Covid Project]..CovidVaccinations$ vac
on dea.location = vac.location and
	dea.date = vac.date
where dea.continent is not null
--order by 2,3 desc

Select *
From PercenPopulationVaccinated

-- Create View of global death
Create View GlobalDeath as
Select continent, Max(cast(total_deaths as int)) as TotalDeathByContinent
From [Covid Project]..CovidDeaths$
Where continent is not null
Group by continent

Select *
From GlobalDeath


--Test case per day
Select vac.date, vac.new_tests, dea.new_cases
From [Covid Project]..CovidVaccinations$ vac
join [Covid Project]..CovidDeaths$ dea
	on vac.date = dea.date
