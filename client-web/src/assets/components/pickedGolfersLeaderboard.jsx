import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const PickedGolfersLeaderboard = ({ seasonId, tournamentId }) => {
  return (
    <Table stickyHeader size='small' className='py-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colspan='6'>Picked Golfers Leaderboard</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Current Place</StyledTableCell>
          <StyledTableCell align='center'>Overall Score</StyledTableCell>
          <StyledTableCell align='center'>Thru</StyledTableCell>
          <StyledTableCell align='center'>Today's Score</StyledTableCell>
          <StyledTableCell align='center'>Times Picked</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          // TODO - render table data here
        }
      </TableBody>
    </Table>
  );
}

export default PickedGolfersLeaderboard;