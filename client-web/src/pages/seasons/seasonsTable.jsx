import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import SeasonsApi from 'src/api/season';

const SeasonsTable = () => {
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    SeasonsApi.list().then(
      (response) => {
        if (response.data.length > 0) {
          setTableData(response.data.sort((a,b) => b.year - a.year));
        }
      })
  }, []);

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={6}>Seasons</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Year</StyledTableCell>
          <StyledTableCell align='center'>Alias</StyledTableCell>
          <StyledTableCell align='center'>Registration Cutoff</StyledTableCell>
          <StyledTableCell align='center' colSpan={2}></StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        { tableData.length > 0 ? 
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>{row.year}</StyledTableCell>
                <StyledTableCell align='center'>{row.alias}</StyledTableCell>
                <StyledTableCell align='center'>{row.registration_cutoff}</StyledTableCell>
                <StyledTableCell align='center'><Button disabled variant='contained' color='primary'>Edit</Button></StyledTableCell>
                <StyledTableCell align='center'><Button disabled variant='contained' color='error'>Delete</Button></StyledTableCell>
              </StyledTableRow>
            ))
          :
            <StyledTableRow key='loading'>
              <StyledTableCell align='center' colSpan={6}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  )
}

export default SeasonsTable;