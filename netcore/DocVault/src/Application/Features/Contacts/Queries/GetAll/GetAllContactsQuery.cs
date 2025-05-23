﻿//------------------------------------------------------------------------------
// <auto-generated>
//     This file is part of the DocVault project.
//     Licensed to the .NET Foundation under the MIT license.
//     See the LICENSE file in the project root for more information.
//
//     Author: neozhu
//     Created Date: 2025-03-19
//     Last Modified: 2025-03-19
//     Description: 
//       Defines a query to retrieve all contacts from the database. The result 
//       is cached to improve performance and reduce database load for repeated 
//       queries.
// </auto-generated>
//------------------------------------------------------------------------------
#nullable enable
using DocVault.Application.Features.Contacts.DTOs;
using DocVault.Application.Features.Contacts.Caching;

namespace DocVault.Application.Features.Contacts.Queries.GetAll;

public class GetAllContactsQuery : ICacheableRequest<IEnumerable<ContactDto>>
{
   public string CacheKey => ContactCacheKey.GetAllCacheKey;
   public IEnumerable<string>? Tags => ContactCacheKey.Tags;
}

public class GetAllContactsQueryHandler :
     IRequestHandler<GetAllContactsQuery, IEnumerable<ContactDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;
    public GetAllContactsQueryHandler(
        IMapper mapper,
        IApplicationDbContext context)
    {
        _mapper = mapper;
        _context = context;
    }

    public async Task<IEnumerable<ContactDto>> Handle(GetAllContactsQuery request, CancellationToken cancellationToken)
    {
        var data = await _context.Contacts.ProjectTo<ContactDto>(_mapper.ConfigurationProvider)
                                                .AsNoTracking()
                                                .ToListAsync(cancellationToken);
        return data;
    }
}


