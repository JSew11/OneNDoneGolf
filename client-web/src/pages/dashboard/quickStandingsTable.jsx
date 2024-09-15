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
                'name': response.data[standingsIndex]['user_details']['username'],
                'prize_money': response.data[standingsIndex]['prize_money'],
                'tournament_wins': response.data[standingsIndex]['tournaments_won']
              })
            }
            // TODO - sort standingsData by prize money before displaying it in the table
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
        <StyledTableRow>
          <StyledTitleCell colSpan='4'>Current Season Standings</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow>
          <StyledTableCell align='center'>Rank</StyledTableCell>
          <StyledTableCell>Name</StyledTableCell>
          <StyledTableCell>Prize Money</StyledTableCell>
          <StyledTableCell>Tournament Wins</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId || standingsRows.length < 1 ?
          // render table data
          standingsRows.map((row) => (
          <StyledTableRow>
            <StyledTableCell align='center'>RANK</StyledTableCell>
            <StyledTableCell>{row['name']}</StyledTableCell>
            <StyledTableCell>{row['prize_money']}</StyledTableCell>
            <StyledTableCell>{row['tournament_wins']}</StyledTableCell>
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