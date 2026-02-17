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
import SeasonGolfersApi from 'src/api/seasonGolfer';

const OWGRTable = ({ seasonId }) => {

  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    if (seasonId) {
      SeasonGolfersApi.list(seasonId).then(
        (response) => {
          const golferSeasonData = [];
          for (let golferSeason of response.data) {
            golferSeasonData.push({
              'id': golferSeason.id,
              'golfer': golferSeason.golfer.first_name + ' ' + golferSeason.golfer.last_name,
              'timesPicked': golferSeason.times_picked,
              'remainingPicks': golferSeason.remaining_available_picks,
              'timesPickedAsWinner': golferSeason.times_picked_as_winner
            });
          }
          setTableData(golferSeasonData);
        }
      );
    }
  }, [seasonId]);

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={5}>Official World Golf Rankings</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Rank</StyledTableCell>
          <StyledTableCell align='center'>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Times Picked</StyledTableCell>
          <StyledTableCell align='center'>Remaining Picks</StyledTableCell>
          <StyledTableCell align='center'>Times Picked as Winner</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && tableData.length > 0 ?
            // render table data
            tableData.map((row) => (
              <StyledTableRow key={row.id}>
                <StyledTableCell align='center'>N/A</StyledTableCell>
                <StyledTableCell align='center'>{row.golfer}</StyledTableCell>
                <StyledTableCell align='center'>{row.timesPicked}</StyledTableCell>
                <StyledTableCell align='center'>{row.remainingPicks}</StyledTableCell>
                <StyledTableCell align='center'>{row.timesPickedAsWinner}</StyledTableCell>
              </StyledTableRow>
            ))
          :
            <StyledTableRow key='loading'>
              <StyledTableCell align='center' colSpan={5}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  );

};

export default OWGRTable;