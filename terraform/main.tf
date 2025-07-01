resource "azurerm_resource_group" "app-rg" {
  name     = "app-rg"
  location = "westus"
}

resource "azurerm_container_group" "example" {
  name                = "api-enrichment-app"
  location            = azurerm_resource_group.app-rg.location
  resource_group_name = azurerm_resource_group.app-rg.name
  ip_address_type     = "Public"
  dns_name_label      = "droidm128-databricks-api-data-enrichment"
  os_type             = "Linux"

  container {
    name   = "api-app"
    image  = "ghcr.io/droidm128/databricks-api-data-enrichment/api-app:latest"
    cpu    = "1"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }
    ports {
      port     = 5000
      protocol = "TCP"
    }

  }
}