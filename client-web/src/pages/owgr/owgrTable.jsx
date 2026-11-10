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
import SeasonGolfersApi from 'src/api/seasonGolfer';

const OWGRTable = ({ seasonId, isAdminUser }) => {

  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    if (seasonId) {
      SeasonGolfersApi.list(seasonId).then(
        (response) => {
          const golferSeasonData = [];
          for (let golferSeason of response.data) {
            if (golferSeason.rank !== null) {
              golferSeasonData.push({
                'id': golferSeason.id,
                'rank': golferSeason.rank,
                'golfer': golferSeason.golfer.first_name + ' ' + golferSeason.golfer.last_name,
                'timesPicked': golferSeason.times_picked,
                'remainingPicks': golferSeason.remaining_available_picks,
                'timesPickedAsWinner': golferSeason.times_picked_as_winner
              });
            }
          }
          setTableData(golferSeasonData.sort((a, b) => a.rank - b.rank));
        }
      );
    }
  }, [seasonId]);

  const handleUpdateOWGRClicked = async () => {
    await SeasonsApi.updateOWGR(seasonId);
  };

  return (
    <Table size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={isAdminUser ? 4 : 5}>Official World Golf Rankings</StyledTitleCell>
          { isAdminUser &&
            <StyledTitleCell>
              <Button
                variant='contained'
                color='secondary'
                onClick={() => handleUpdateOWGRClicked()}
              >Update OWGR</Button>
            </StyledTitleCell>
          }
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
                <StyledTableCell align='center'>{row.rank}</StyledTableCell>
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