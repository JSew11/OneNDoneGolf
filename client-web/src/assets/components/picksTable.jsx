import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import { jwtDecode } from 'jwt-decode';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import PicksApi from 'src/api/pick';

const PicksTable = ({ seasonId }) => {

  const [tableData, setTableData] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);
  
  const { access } = useSelector(state => state.auth);
  
  useEffect(() => {
    if (access !== null) {
      setSelectedUserId(jwtDecode(access)['id'])
    }
  }, [access]);

  useEffect(() => {
    if (seasonId !== null && selectedUserId !== null) {
      PicksApi.list(seasonId, selectedUserId).then(
        (response) => {
          const pickData = [];
          for (let pickIndex in response.data) {
            const pick = response.data[pickIndex];
            pickData.push({
              id: pick['id'],
              tournament: pick['tournament'] ? 
                  pick['tournament']['name']
                :
                  '--',
              golfer: pick['scored_golfer'] ? 
                  pick['scored_golfer']['first_name'] + ' ' + pick['scored_golfer']['last_name']
                :
                  '--',
              place: 'TODO - get this',
              prizeMoney: 'TODO - get this'
            });
          }
          setTableData(pickData);
        }
      );
    }
  }, [selectedUserId]);

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={4}>{
              seasonId ?
                'TODO - dropdown to select user'
              :
                'Loading Table Data'
            }
          </StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Tournament</StyledTableCell>
          <StyledTableCell align='center'>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Place</StyledTableCell>
          <StyledTableCell align='center'>Prize Money</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && selectedUserId && tableData.length > 0 ?
            // TODO - render table data
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>{row.tournament}</StyledTableCell>
                <StyledTableCell align='center'>{row.golfer}</StyledTableCell>
                <StyledTableCell align='center'>{row.place}</StyledTableCell>
                <StyledTableCell align='center'>{row.prizeMoney}</StyledTableCell>
              </StyledTableRow>
            ))
          :
            <StyledTableRow key='loading'>
              <StyledTableCell align='center' colSpan={11}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  );
}

export default PicksTable;