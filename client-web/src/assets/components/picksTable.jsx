import { useEffect, useState } from 'react';
import { useTheme } from '@mui/material';
import { useSelector } from 'react-redux';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { jwtDecode } from 'jwt-decode';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import PicksApi from 'src/api/pick';
import SeasonUsersApi from 'src/api/seasonUser';

const PicksTable = ({ seasonId }) => {
  const theme = useTheme();

  const [tableData, setTableData] = useState([]);
  const [seasonUsers, setSeasonUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [selectedUserTotals, setSelectedUserTotals] = useState([]);
  
  const { access } = useSelector(state => state.auth);

  useEffect(() => {
    if (seasonId) {
      SeasonUsersApi.list(seasonId).then(
        (response) => {
          if (response.status === 200) {
            const seasonUserData = [];
            for (let seasonUsersIndex in response.data) {
              seasonUserData.push({
                id: response.data[seasonUsersIndex]['user']['id'],
                username: response.data[seasonUsersIndex]['user']['username']
              });
            }
            setSeasonUsers(seasonUserData);
          }
        },
        (error) => error
      );
    }
  }, [seasonId]);

  useEffect(() => {
    if (access) {
      const decodedToken = jwtDecode(access);
      const selectedUser = {
        id: decodedToken['id'],
        username: decodedToken['username']
      };
      setSeasonUsers([selectedUser])
      setSelectedUserId(selectedUser['id']);
    }
  }, [access]);

  useEffect(() => {
    if (seasonId && selectedUserId) {
      SeasonUsersApi.retrieve(seasonId, selectedUserId).then(
        (response) => {
          setSelectedUserTotals({
            'winnings': response.data['prize_money'] ?
                '$' + Number(response.data['prize_money']).toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
              :
                'N/A',
            'rank': response.data['rank'] ?? 'N/A',
            'cash_won': response.data['cash_won'] ?? 'N/A'
        })
        }
      );

      PicksApi.list(seasonId, selectedUserId).then(
        (response) => {
          const pickData = [];
          for (let pickIndex in response.data) {
            const pick = response.data[pickIndex];
            pickData.push({
              id: pick['id'],
              tournament_scored: (pick['scored_golfer'] != null),
              tournament: pick['tournament'] ? 
                  pick['tournament']['name']
                :
                  '',
              golfer: pick['scored_golfer'] ? 
                  pick['scored_golfer']['first_name'] + ' ' + pick['scored_golfer']['last_name']
                :
                  '--',
              place: pick['position'] ?? '--',
              prizeMoney: pick['prize_money'] ? 
                '$' + Number(pick['prize_money']).toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
              :
                '--'
            });
          }
          setTableData(pickData);
        }
      );
    }
  }, [seasonId, selectedUserId]);

  const handleChange = (event)=> {
    setSelectedUserId(event.target.value);
  }

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={4}>{
              seasonId && selectedUserId ?
                <FormControl fullWidth>
                  <InputLabel
                    id='user-select-label'
                    sx={{
                      color: theme.palette.primary.contrastText,
                      '&.Mui-focused': {
                        color: theme.palette.primary.contrastText
                      }
                    }}
                  >
                    User
                  </InputLabel>
                  <Select
                    labelId='user-select-label'
                    id='user-select'
                    value={selectedUserId}
                    label='User'
                    onChange={handleChange}
                    sx={{
                      color: theme.palette.primary.contrastText,
                      '.MuiOutlinedInput-notchedOutline': {
                        borderColor: theme.palette.primary.contrastText,
                      },
                      '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: theme.palette.primary.contrastText,
                      },
                      '&:hover .MuiOutlinedInput-notchedOutline': {
                        borderColor: theme.palette.primary.contrastText,
                      },
                      '.MuiSvgIcon-root ': {
                        fill: theme.palette.primary.contrastText,
                      }
                    }}
                  >
                    {
                      seasonUsers.map((seasonUser) => (
                        <MenuItem key={seasonUser.id} value={seasonUser.id}>
                          {seasonUser.username}
                        </MenuItem>
                      ))
                    }
                  </Select>
                </FormControl>
              :
                'Loading Table Data'
            }
          </StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='totals'>
          <StyledTableCell></StyledTableCell>
          <StyledTableCell align='center'><b>Winnings:</b> {selectedUserTotals['winnings']}</StyledTableCell>
          <StyledTableCell align='center'><b>Rank:</b> {selectedUserTotals['rank']}</StyledTableCell>
          <StyledTableCell align='center'><b>Cash Won:</b> {selectedUserTotals['cash_won']}</StyledTableCell>
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
            // render table data
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>{row.tournament}</StyledTableCell>
                {
                  row.tournament_scored ?
                    <>
                      <StyledTableCell align='center'>{row.golfer}</StyledTableCell>
                      <StyledTableCell align='center'>{row.place}</StyledTableCell>
                      <StyledTableCell align='center'>{row.prizeMoney}</StyledTableCell>
                    </>
                  :
                    <StyledTableCell align='center' colSpan='3'>
                      -- Tournament has not yet been scored --
                    </StyledTableCell>
                }
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