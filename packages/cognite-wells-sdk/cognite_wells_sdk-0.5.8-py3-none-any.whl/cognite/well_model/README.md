# Installation with pip

```bash
pip install cognite-wells-sdk
```

# Usage

## Authenticating and creating a client

### With environment variables

**NOTE**: *must be valid for both cdf and geospatial API*

```bash
export COGNITE_PROJECT=<project-tenant>
export COGNITE_API_KEY=<your-api-key>
```

You can then initialize the client with
```py
from cognite.well_model import CogniteWellsClient
wells_client = CogniteWellsClient()
```

### Without environment variables

Alternatively, the client can be initialized like this:

```python
import os
from cognite.well_model import CogniteWellsClient
api_key = os.environ["COGNITE_API_KEY"]
wells_client = CogniteWellsClient(project="your-project", api_key=api_key)
```

### Connect to a different CDF environment

```py
from cognite.well_model import CogniteWellsClient, Cluster
wells_client = CogniteWellsClient(cluster = Cluster.BP)
```


## **Well queries**

### Get well by id

```python
well = wells_client.wells.get_by_id(8456650753594878)
```

### List wells

```python
wells = wells_client.wells.list()
```

#### Filter wells by wkt polygon

```python
from cognite.well_model.models import PolygonFilter

polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(polygon=PolygonFilter(geometry=polygon, crs="epsg:4326"))
```

#### Filter wells by wkt polygon, name/description and specify desired outputCrs

```python
polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(
    polygon=PolygonFilter(geometry=polygon, crs="epsg:4326", geometry_type="WKT"),
    string_matching="16/",
    output_crs="EPSG:23031"
)
```

### Get wells that have a trajectory

```python
from cognite.well_model.models import TrajectoryFilter

wells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(), limit=None)
```

### Get wells that have a trajectory with data between certain depths

```python
wells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(min_depth=1400.0, max_depth=1500.0), limit=None)
```

### Get wells that has the right set of measurement types

```python
from cognite.well_model.models import MeasurementFilter, MeasurementFilters, MeasurementType

gammarayFilter = MeasurementFilter(measurement_type=MeasurementType.gamma_ray)
densityFilter = MeasurementFilter(measurement_type=MeasurementType.density)

# Get wells with all measurements
measurements_filter = MeasurementFilters(contains_all=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)

# Or get wells with any of the measurements
measurements_filter = MeasurementFilters(contains_any=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)
```

### Get wellbores for a well id

```python
wellbores = wells_client.wellbores.get_from_well(well.id)
```

or

```python
well = wells_client.wells.get_by_id(519497487848)
wellbores = well.wellbores()
```

### Get wellbores from multiple well ids

```python
wellbores = wells_client.wellbores.get_from_wells([17257290836510, 8990585729991697])
```

### Filter - list all labels

```python
blocks = wells_client.wells.blocks()
fields = wells_client.wells.fields()
operators = wells_client.wells.operators()
quadrants = wells_client.wells.quadrants()
sources = wells_client.wells.sources()
measurementTypes = wells_client.wells.measurements()
```

## Wellbore queries

### Get wellbore by id

```jupyterpython
wellbore = wells_client.wellbores.get_by_id(2360682364100853)
```

### Get wellbore measurement for measurementType: 'GammaRay'

```python
measurements = wells_client.wellbores.get_measurement(wellbore_id=2360682364100853, measurement_type=MeasurementType.gamma_ray)
```

### Get trajectory for a wellbore

```python
wellbore = wells_client.wellbores.get_by_id(2360682364100853)
trajectory = wellbore.trajectory()
```

Or get it directly from a wellbore id

```python
trajectory = wells_client.surveys.get_trajectory(2360682364100853)
```

## Survey queries

### Get data from a survey, from start and end rows

```python
trajectory_data = wells_client.surveys.get_data(17257290836510, start=0, end=100000, columns=["MD", "AZIMUTH"])
```

### Get all data from a survey object
```python
trajectory = wells_client.surveys.get_trajectory(2360682364100853)
trajectory_data = trajectory.data()
```

## Ingestion

### Initialise tenant

Before ingesting any wells, the tenant must be initialized to add in the standard assets and labels used in the WDL.

```python
from cognite.well_model import CogniteWellsClient

wells_client = CogniteWellsClient()
log_output = wells_client.ingestion.ingestion_init()
print(log_output)  # If something is wrong with authorization, you should see that in the logs
```

### Add source

Before ingestion from a source can take place, the source must be registered in WDL.

```python
import os
from cognite.well_model import CogniteWellsClient

wells_client = CogniteWellsClient()
created_sources = wells_client.sources.ingest_sources(["Source1, Source2"])
```

### Ingest wells
```python
import os
from datetime import date

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleWithUnit, WellDatum, Wellhead, WellIngestion

wells_client = CogniteWellsClient()
source_asset_id = 102948135620745 # Id of the well source asset in cdf

well_to_create = WellIngestion(
    asset_id=source_asset_id,
    well_name="well-name",
    description="Optional description for the well",
    country="Norway",
    quadrant="25",
    block="25/5",
    field="Example",
    operator="Operator1",
    spud_date=date(2021, 3, 17),
    water_depth=0.0,
    water_depth_unit="meters",
    wellhead=Wellhead(
        x = 21.0,
        y = 42.0,
        crs = "EPSG:4236" # Must be a EPSG code
    ),
    datum=WellDatum(
        elevation = DoubleWithUnit(value=1.0, unit="meters"),
        reference = "well-datum-reference",
        name = "well-datum-name"
    ),
    source="Source System Name"
)

wells_client.ingestion.ingest_wells([well_to_create]) # Can add multiple WellIngestion objects at once
```

### Ingest wellbores with optional well and/or trajectory
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import (
    DoubleArrayWithUnit,
    TrajectoryIngestion,    
    WellIngestion,
    WellboreIngestion,
    ParentType,
    MeasurementIngestion,
    MeasurementField,
    MeasurementType
)

wells_client = CogniteWellsClient()
source_asset_id = 102948135620745 # Id of the wellbore source asset in cdf
source_trajectory_ext_id = "some sequence ext id" # Id of the source sequence in cdf

well_to_create = WellIngestion(...)
trajectory_to_create = TrajectoryIngestion(
    source_sequence_ext_id=source_trajectory_ext_id,
    measured_depths = DoubleArrayWithUnit(values=[0.0, 1.0, 2.0], unit="meters"),
    inclinations = DoubleArrayWithUnit(values=[10.0, 1.0, 22.0], unit="degrees"),
    azimuths = DoubleArrayWithUnit(values=[80.0, 81.0, 82.0], unit="degrees")
)
measurements_to_create = [
    MeasurementIngestion(
        sequence_external_id="measurement_sequence_1",
        measurement_fields=[
            MeasurementField(type_name=MeasurementType.gamma_ray),
            MeasurementField(type_name=MeasurementType.density),
        ],
    ),
    MeasurementIngestion(
        sequence_external_id="measurement_sequence_2",
        measurement_fields=[
            MeasurementField(type_name=MeasurementType.geomechanics),
            MeasurementField(type_name=MeasurementType.lot),
        ],
    )   
]

wellbore_to_create = WellboreIngestion(
    asset_id = source_asset_id,
    wellbore_name = "wellbore name",
    parent_name = "name of parent well or wellbore",
    parent_type = ParentType.well, # or ParentType.wellbore
    well_name = "name of parent well", # top level well; required in addition to the parent name (even if parent is well)
    source = "Source System Name",
    trajectory_ingestion = trajectory_to_create,
    measurement_ingestions = measurements_to_create,
    well_ingestion = well_to_create # if not ingesting a well, then one must already exist
)

wells_client.ingestion.ingest_wellbores([wellbore_to_create]) # Can add multiple WellboreIngestion objects at once
```

### Ingest casing data
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleArrayWithUnit, CasingIngestion

wells_client = CogniteWellsClient()
source_casing_id = 102948135620745 # Id of the casing source sequence in cdf


casing_to_ingest = CasingIngestion(
    source_casing_id = source_casing_id,
    wellbore_name = "wellbore name",
    casing_name = "Surface Casing",
    body_inside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),
    body_outside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),
    md_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"),
    md_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m"),
    tvd_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"), # TVD measurements are optional
    tvd_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m") # TVD measurements are optional
)

wells_client.ingestion.ingest_casings([casing_to_ingest]) # Can add multiple CasingIngestion objects at once
```
