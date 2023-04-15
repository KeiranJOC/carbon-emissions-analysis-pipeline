resource "google_bigquery_dataset" "dataset_raw" {
  dataset_id = var.bq_dataset_raw
  project    = var.project
  location   = var.region
}

# resource "google_bigquery_dataset" "dataset" {
#   dataset_id = var.bq_dataset
#   project    = var.project
#   location   = var.region
# }

resource "google_bigquery_table" "energy_consumption" {
  dataset_id          = google_bigquery_dataset.dataset_raw.dataset_id
  table_id            = "energy_consumption_raw"
  deletion_protection = false

  time_partitioning {
    type  = "MONTH"
    field = "date"
  }

  schema = <<EOF
[
  {
    "name": "site",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "meter",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "unit",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "NULLABLE"
  },
  {
    "name": "0000",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0030",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0100",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0130",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0200",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0230",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0300",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0330",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0400",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0430",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0500",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0530",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0600",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0630",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0700",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0730",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0800",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0830",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0900",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "0930",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1000",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1030",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1100",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1130",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1200",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1230",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1300",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1330",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1400",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1430",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1500",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1530",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1600",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1630",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1700",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1730",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1800",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1830",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1900",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "1930",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2000",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2030",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2100",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2130",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2200",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2230",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2300",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "2330",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}

resource "google_bigquery_table" "conversion_factors" {
  dataset_id          = google_bigquery_dataset.dataset_raw.dataset_id
  table_id            = "conversion_factors_raw"
  deletion_protection = false

  clustering = [
    "scope",
    "level_1",
    "level_2",
    "level_3"
  ]

  schema = <<EOF
[
  {
    "name": "scope",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "level_1",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "level_2",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "level_3",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "level_4",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "column_text",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "uom",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "ghg_unit",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "ghg_conversion_factor_2022",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

}
