using System.Threading;
using System.Threading.Tasks;
using DocVault.Application.Common.Interfaces;
using DocVault.Application.Common.Interfaces.Identity;
using DocVault.Application.Features.Products.Commands.AddEdit;
using DocVault.Application.Pipeline.PreProcessors;
using Microsoft.Extensions.Logging;
using Moq;
using NUnit.Framework;

namespace DocVault.Application.UnitTests.Common.Behaviours;

public class RequestLoggerTests
{
    private readonly Mock<ICurrentUserAccessor> _currentUserAccessor;
    private readonly Mock<IIdentityService> _identityService;
    private readonly Mock<ILogger<AddEditProductCommand>> _logger;

    public RequestLoggerTests()
    {
        _currentUserAccessor = new Mock<ICurrentUserAccessor>();
        _identityService = new Mock<IIdentityService>();
        _logger = new Mock<ILogger<AddEditProductCommand>>();
    }

    [Test]
    public async Task ShouldCallGetUserNameAsyncOnceIfAuthenticated()
    {
        _currentUserAccessor.Setup(x => x.SessionInfo).Returns(new SessionInfo("Administrator", "Administrator", "","","","", UserPresence.Available));
        var requestLogger = new LoggingPreProcessor<AddEditProductCommand>(_logger.Object, _currentUserAccessor.Object);
        await requestLogger.Process(
            new AddEditProductCommand { Brand = "Brand", Name = "Brand", Price = 1.0m, Unit = "EA" },
            new CancellationToken());
        _currentUserAccessor.Verify(i => i.SessionInfo, Times.Once);
    }

    [Test]
    public async Task ShouldNotCallGetUserNameAsyncOnceIfUnauthenticated()
    {
        var requestLogger = new LoggingPreProcessor<AddEditProductCommand>(_logger.Object, _currentUserAccessor.Object);
        await requestLogger.Process(
            new AddEditProductCommand { Brand = "Brand", Name = "Brand", Price = 1.0m, Unit = "EA" },
            new CancellationToken());
        _identityService.Verify(i => i.GetUserNameAsync(It.IsAny<string>(), CancellationToken.None), Times.Never);
    }
}