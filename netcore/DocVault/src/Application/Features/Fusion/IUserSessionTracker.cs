using ActualLab.Fusion;
using DocVault.Application.Common.Interfaces.Identity;

namespace DocVault.Application.Features.Fusion;

public interface IUserSessionTracker: IComputeService
{
    Task AddUserSession(string pageComponent, SessionInfo sessionInfo, CancellationToken cancellationToken = default);
    Task RemoveUserSession(string pageComponent,string userId,  CancellationToken cancellationToken = default);
    Task RemoveAllSessions(string userId, CancellationToken cancellationToken = default);
   
    [ComputeMethod]
    Task<List<SessionInfo>> GetUserSessions(string pageComponent,CancellationToken cancellationToken = default);
}
