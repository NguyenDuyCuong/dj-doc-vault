using DocVault.Application.Features.PicklistSets.DTOs;

namespace DocVault.Application.Common.Interfaces;

public interface IPicklistService
{
    List<PicklistSetDto> DataSource { get; }
    event Func<Task>? OnChange;
    void Initialize();
    void Refresh();
}