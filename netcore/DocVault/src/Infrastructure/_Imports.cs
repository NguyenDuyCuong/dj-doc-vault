// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

global using System.Security.Claims;
global using AutoMapper;
global using AutoMapper.QueryableExtensions;
global using DocVault.Application.Common.Interfaces;
global using DocVault.Application.Common.Interfaces.Identity;
global using DocVault.Application.Common.Models;
global using DocVault.Infrastructure.Persistence;
global using DocVault.Infrastructure.Persistence.Extensions;
global using DocVault.Infrastructure.Services;
global using DocVault.Infrastructure.Services.Identity;
global using DocVault.Domain.Entities;
global using Microsoft.AspNetCore.Components.Authorization;
global using Microsoft.AspNetCore.Identity;
global using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
global using Microsoft.EntityFrameworkCore;
global using Microsoft.Extensions.DependencyInjection;
global using Microsoft.Extensions.Logging;
global using Microsoft.Extensions.Options;