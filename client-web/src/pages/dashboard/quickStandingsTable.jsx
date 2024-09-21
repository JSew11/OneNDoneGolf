import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';

import SeasonsApi from 'src/api/season';
import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const QuickStandingsTable = ({ seasonId }) => {
  const [standingsRows, setStandingsRows] = useState([]);

  useEffect(() => {
    if (seasonId) {
      SeasonsApi.standings(seasonId).then(
        (response) => {
          if (response.status === 200) {
            const standingsData = [];
            for (let standingsIndex in response.data) {
              standingsData.push({
                'id': response.data[standingsIndex]['id'],
                'rank': Number(standingsIndex) + 1,
                'name': response.data[standingsIndex]['user_details']['username'],
                'prize_money': response.data[standingsIndex]['prize_money'],
                'tournament_wins': response.data[standingsIndex]['tournaments_won']
              })
            }
            setStandingsRows(standingsData);
          }
        },
        (error) => error
      );
    }
  }, [seasonId]);

  return (
    <Table stickyHeader size='small' className='py-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan='4'>Current Season Standings</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Rank</StyledTableCell>
          <StyledTableCell>Name</StyledTableCell>
          <StyledTableCell align='center'>Prize Money</StyledTableCell>
          <StyledTableCell align='center'>Tournament Wins</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId || standingsRows.length < 1 ?
          // render table data
          standingsRows.map((row) => (
            <StyledTableRow key={row.id}>
              <StyledTableCell align='center'>{row.rank}</StyledTableCell>
              <StyledTableCell>{row.name}</StyledTableCell>
              <StyledTableCell align='center'>{'$' + Number(row.prize_money).toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')}</StyledTableCell>
              <StyledTableCell align='center'>{row.tournament_wins}</StyledTableCell>
            </StyledTableRow>
          )) :
          // loading circle
          <StyledTableRow>
            <StyledTableCell align='center' colSpan='4'>
              <CircularProgress className='my-4' size='50px'/>
            </StyledTableCell>
          </StyledTableRow>
        }
      </TableBody>
    </Table>
  );
};

export default QuickStandingsTable;