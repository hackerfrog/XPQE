## XPQE
> Cross Platform Query Editor

## Overview
A single application from which you can connect and execute query from single file on different platform.

## Supported Engines
|Engine|Status|
|---|---|
| `MySQL` | :heavy_check_mark: Available |
| `PostgreSQL` | :runner: WIP |

## Shortcuts
|Shortcut|Detail|
|---|---|
| `Ctrl + Enter` | Run selected query |
| `Ctrl + /` | Toggle comment |

## How to setup server profile
1. Launch Editor
1. Click on `Manage` inside `Profile` menu.
1. Click of `Add` button to add new server.
1. Give `Profile Name` of your choice. (This will used during query as identifier)
1. Fill remaining details of your server.
1. `Test connection` to validate your details.
1. Click `Save` to save profile.

```sql
-- Run query on server profile `profile1`
@profile1:SELECT * FROM users limit 10

-- Run query on server profile `profile1`
@profile2:SELECT * FROM users limit 10
```

## LICENSE

  Copyright © 2020 Lovepreet Singh

  This program is free software; you can redistribute it and/or modify it under
  the terms of the GNU General Public License as published by the Free Software
  Foundation; either version 3 of the License, or (at your option) any later
  version.

  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with
  this program. If not, see <http://www.gnu.org/licenses/>.