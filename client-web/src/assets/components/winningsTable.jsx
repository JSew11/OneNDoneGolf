import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';

const WinningsTable = ({ seasonId }) => {

  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    if (seasonId) {
      // TODO - populate table data
    }
  }, [seasonId]);

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={10}>Tournament Winners</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell colSpan={3} align='center'>Tournament</StyledTableCell>
          <StyledTableCell colSpan={3} align='center'>Winner(s)</StyledTableCell>
          <StyledTableCell colSpan={3} align='center'>Picked Golfer(s)</StyledTableCell>
          <StyledTableCell colSpan={1} align='center'>Place</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && tableData.length > 0 ?
            // render table data
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell colSpan={3} align='center'>{row.tournament}</StyledTableCell>
                <StyledTableCell colSpan={3} align='center'>{row.winners}</StyledTableCell>
                <StyledTableCell colSpan={3} align='center'>{row.golfers}</StyledTableCell>
                <StyledTableCell colSpan={1} align='center'>{row.place}</StyledTableCell>
              </StyledTableRow>
            ))
          :
            <StyledTableRow key='loading'>
              <StyledTableCell align='center' colSpan={10}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  );
};

export default WinningsTable;