import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from '@mui/material/Button';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import UsersApi from 'src/api/user';

const UsersTable = () => {
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    UsersApi.list().then(
      (response) => {
        if (response.data.results.length > 0) {
          setTableData(response.data.results);
        }
      }
    )
  }, [])

  return (
    <Table size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={5}>Users</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Username</StyledTableCell>
          <StyledTableCell align='center'>Email</StyledTableCell>
          <StyledTableCell align='center'>Name</StyledTableCell>
          <StyledTableCell align='center'>Payment Method</StyledTableCell>
          <StyledTableCell></StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        { tableData.length > 0 ? 
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>{row.username}</StyledTableCell>
                <StyledTableCell align='center'>{row.email}</StyledTableCell>
                <StyledTableCell align='center'>{(row.first_name ?? '') + (row.last_name ? ' ' + row.last_name : '')}</StyledTableCell>
                <StyledTableCell align='center'>{row.payment_method}</StyledTableCell>
                <StyledTableCell>
                  <ButtonGroup size='small' variant='contained' aria-label='user-row-actions'>
                    <Button>Edit</Button>
                    <Button color='error'>Delete</Button>
                  </ButtonGroup>
                </StyledTableCell>
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
};

export default UsersTable;