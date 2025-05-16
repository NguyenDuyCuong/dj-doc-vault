using DocVault.Application.Features.Identity.DTOs;

namespace DocVault.Application.Common.Interfaces.Identity;

public interface IUserService
{
    List<ApplicationUserDto> DataSource { get; }
    event Func<Task>? OnChange;
    void Initialize();
    void Refresh();
}