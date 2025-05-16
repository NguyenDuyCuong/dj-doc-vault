using DocVault.Application.Features.Tenants.DTOs;

namespace DocVault.Application.Common.Interfaces.MultiTenant;

public interface ITenantService
{
    List<TenantDto> DataSource { get; }
    event Func<Task>? OnChange;
    void Initialize();
    void Refresh();
}