import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';

const WinningsTable = () => {
  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead></TableHead>
      <TableBody></TableBody>
    </Table>
  );
};

export default WinningsTable;