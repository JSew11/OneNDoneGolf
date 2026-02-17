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
import SeasonTournamentsApi from 'src/api/seasonTournament';

const TournamentScheduleTable = ({ seasonId }) => {

  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    if (seasonId) {
      SeasonTournamentsApi.list(seasonId).then(
        (response) => {
          const tournamentSeasonData = [];
          for (let tournamentSeason of response.data) {
            tournamentSeasonData.push({
              'id': tournamentSeason.id,
              'startDate': new Date(tournamentSeason.start_date).toLocaleDateString('en-us', {
                'dateStyle': 'full'
              }),
              'endDate': new Date(tournamentSeason.end_date).toLocaleDateString('en-us', {
                'dateStyle': 'full'
              }),
              'tournament': tournamentSeason.tournament.name,
            });
          }
          setTableData(tournamentSeasonData);
        }
      );
    }
  }, [seasonId]);

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={10}>Schedule</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Start Date</StyledTableCell>
          <StyledTableCell align='center'>End Date</StyledTableCell>
          <StyledTableCell align='center'>Tournament</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && tableData.length > 0 ?
            // render table data
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>{row.startDate}</StyledTableCell>
                <StyledTableCell align='center'>{row.endDate}</StyledTableCell>
                <StyledTableCell align='center'>{row.tournament}</StyledTableCell>
              </StyledTableRow>
            ))
          :
            <StyledTableRow key='loading'>
              <StyledTableCell align='center' colSpan={3}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  )

};

export default TournamentScheduleTable;