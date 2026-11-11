import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import ButtonConfirm from 'src/assets/components/buttonConfirm';
import UsersApi from 'src/api/user';
import SeasonsApi from 'src/api/season';
import UserModal from 'src/assets/modals/user';

const UsersTable = () => {
  const [activeSeason, setActiveSeason] = useState(null);
  const [fullUserList, setFullUserList] = useState([]);
  const [loadTableData, setLoadTableData] = useState(true);

  const [tableData, setTableData] = useState([]);
  const [showInactiveUsers, setShowInactiveUsers] = useState(false);
  const [reloadTableFilters, setReloadTableFilters] = useState(false);

  const paymentMethodMap = {
    'venmo': 'Venmo',
    'cash_app': 'Cash App',
    'paypal': 'PayPal',
    'zelle': 'Zelle'
  }

  useEffect(() => {
    SeasonsApi.active().then((response) => {
      setActiveSeason(response.data);
    })
  }, [])

  useEffect(() => {
    if (loadTableData) {
      UsersApi.list().then(
        (response) => {
          if (response.data.results.length > 0) {
            setFullUserList(response.data.results);
            setReloadTableFilters(true);
            setLoadTableData(false);
          }
        }
      )
    }
  }, [loadTableData])

  useEffect(() => {
    if (reloadTableFilters) {
      setTableData(fullUserList.filter((user) => {
        if (!showInactiveUsers) {
          return user.active;
        }
        return true;
      }));
      setReloadTableFilters(false);
    }
  }, [reloadTableFilters])
  
  const handleDelete = (userId) => {
    UsersApi.destroy(userId).then(
      (response) => {
        if (response.status === 204) {
          setLoadTableData(true);
        }
      }
    ).catch((error) => error)
  }

  const handleDownloadEmailList = () => {
    const csvEmailList = 'data:text/csv;charset=utf-8,' + tableData.map((user) => user.email + ',').join('\n');
    const encodedCSV = encodeURI(csvEmailList);
    const link = document.createElement('a');
    link.setAttribute('href', encodedCSV);
    link.setAttribute('download', 'one_n_done_email_list_' + new Date().toLocaleDateString('en-US'));
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return (
    <Table size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={4}>Users</StyledTitleCell>
          <StyledTitleCell colSpan={1}>
            <Button
              variant='contained'
              color='secondary'
              onClick={handleDownloadEmailList}
            >Download Email List</Button>
          </StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='filters'>
          <StyledTableCell colSpan={1} sx={{ borderBottom: 0 }}>
            <Button
              variant='contained'
              size='small'
              onClick={() => setReloadTableFilters(true)}
              className='float-start'
            >Apply Filters</Button>
          </StyledTableCell>
          <StyledTableCell colSpan={4} sx={{ borderBottom: 0 }}>
            <Checkbox
              className='py-0 my-0'
              checked={showInactiveUsers}
              onChange={() => setShowInactiveUsers((show) => !show)}
              slotProps={{
                input: { 'aria-label': 'controlled' }
              }}
            /> Show Inactive Users
          </StyledTableCell>
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
            tableData.map((user) => (
              <StyledTableRow key={user.id}>
                <StyledTableCell align='center'>{user.username}</StyledTableCell>
                <StyledTableCell align='center'>{user.email}</StyledTableCell>
                <StyledTableCell align='center'>{(user.first_name ?? '') + (user.last_name ? ' ' + user.last_name : '')}</StyledTableCell>
                <StyledTableCell align='center'>{paymentMethodMap[user.payment_method]}</StyledTableCell>
                <StyledTableCell align='center'>
                  <ButtonGroup size='small' variant='contained' aria-label='user-row-actions'>
                    <UserModal user={user} callback={() => setLoadTableData(true)} seasonId={activeSeason.id}/>
                    <ButtonConfirm
                      onClick={() => handleDelete(user.id)}
                      buttonText='Delete'
                      buttonColor='error'
                      title='Delete this User?'
                      message='Are you sure you want to delete this User?'
                    />
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