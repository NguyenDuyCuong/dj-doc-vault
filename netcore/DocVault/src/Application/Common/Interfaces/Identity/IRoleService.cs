using DocVault.Application.Features.Identity.DTOs;

namespace DocVault.Application.Common.Interfaces.Identity;

public interface IRoleService
{
    List<ApplicationRoleDto> DataSource { get; }
    event Func<Task>? OnChange;
    void Initialize();
    void Refresh();
}