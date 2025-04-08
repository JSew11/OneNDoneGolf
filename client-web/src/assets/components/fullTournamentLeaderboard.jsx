import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const FullTournamentLeaderboard = ({ seasonId, tournamentId }) => {
  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Place</StyledTableCell>
          <StyledTableCell align='center'>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Overall Score</StyledTableCell>
          <StyledTableCell align='center'>Today's Score</StyledTableCell>
          <StyledTableCell align='center'>Thru</StyledTableCell>
          <StyledTableCell align='center'>R1</StyledTableCell>
          <StyledTableCell align='center'>R2</StyledTableCell>
          <StyledTableCell align='center'>R3</StyledTableCell>
          <StyledTableCell align='center'>R4</StyledTableCell>
          <StyledTableCell align='center'>Total</StyledTableCell>
          <StyledTableCell align='center'>Winnings</StyledTableCell>
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

export default FullTournamentLeaderboard;