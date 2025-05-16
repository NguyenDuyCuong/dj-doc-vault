using DocVault.Server.UI.Models.NavigationMenu;

namespace DocVault.Server.UI.Services.Navigation;

public interface IMenuService
{
    IEnumerable<MenuSectionModel> Features { get; }
}