﻿// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

namespace DocVault.Application.Common.Interfaces;

public interface IUploadService
{
    Task<string> UploadAsync(UploadRequest request);
    Task RemoveAsync(string filename);
}