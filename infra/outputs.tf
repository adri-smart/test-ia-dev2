output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "web_app_hostname" {
  value = azurerm_linux_web_app.web_app.default_hostname
}

output "redis_hostname" {
  value = azurerm_redis_cache.redis.hostname
}
