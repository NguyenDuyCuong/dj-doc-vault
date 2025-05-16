using System.Threading.Tasks;
using DocVault.Application.Common.ExceptionHandlers;
using DocVault.Application.Features.PicklistSets.Commands.AddEdit;
using DocVault.Application.Features.PicklistSets.Commands.Delete;
using DocVault.Domain.Entities;
using FluentAssertions;
using NUnit.Framework;

namespace DocVault.Application.IntegrationTests.KeyValues.Commands;

using static Testing;

public class DeletePicklistTests : TestBase
{
    [Test]
    public void ShouldRequireValidKeyValueId()
    {
        var command = new DeletePicklistSetCommand(new[] { 99 });

        FluentActions.Invoking(() =>
            SendAsync(command)).Should().ThrowAsync<NotFoundException>();
    }

    [Test]
    public async Task ShouldDeleteKeyValue()
    {
        var addCommand = new AddEditPicklistSetCommand
        {
            Name = Picklist.Brand,
            Text = "Word",
            Value = "Word",
            Description = "For Test"
        };
        var result = await SendAsync(addCommand);

        await SendAsync(new DeletePicklistSetCommand(new[] { result.Data }));

        var item = await FindAsync<Document>(result.Data);

        item.Should().BeNull();
    }
}