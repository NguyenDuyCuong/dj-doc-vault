﻿// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using DocVault.Domain.Common.Entities;
using DocVault.Domain.Identity;
using Microsoft.EntityFrameworkCore.ChangeTracking;

namespace DocVault.Domain.Entities;

public class AuditTrail : IEntity<int>
{
    public int Id { get; set; }
    public string? UserId { get; set; }
    public virtual ApplicationUser? Owner { get; set; }
    public AuditType AuditType { get; set; }
    public string? TableName { get; set; }
    public DateTime DateTime { get; set; }
    public Dictionary<string, object?>? OldValues { get; set; }
    public Dictionary<string, object?>? NewValues { get; set; }
    public List<string>? AffectedColumns { get; set; }
    public Dictionary<string, object> PrimaryKey { get; set; } = new();
    public List<PropertyEntry> TemporaryProperties { get; } = new();
    public bool HasTemporaryProperties => TemporaryProperties.Any();
    public string? DebugView { get; set; }
    public string? ErrorMessage { get; set; }
}

public enum AuditType
{
    None,
    Create,
    Update,
    Delete
}