import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';

const PicksTable = ({ seasonId }) => {
  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow>
          <StyledTitleCell>{
              seasonId ?
                'TODO - dropdown to select user'
              :
                'Loading Table Data'
            }
          </StyledTitleCell>
        </StyledTableRow>
        {/* TODO - Add filter, and header rows */}
      </TableHead>
      <TableBody>
        {/* TODO - Add data rows */}
      </TableBody>
    </Table>
  );
}

export default PicksTable;