import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const QuickStandingsTable = () => {
  return (
    <Table stickyHeader size='small'
      sx={{}}
    >
      <TableHead>
        <StyledTableRow>
          <StyledTitleCell colSpan='4'>Current Season Standings</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow>
          <StyledTableCell>Rank</StyledTableCell>
          <StyledTableCell>Name</StyledTableCell>
          <StyledTableCell>Prize Money</StyledTableCell>
          <StyledTableCell>Tournament Wins</StyledTableCell>
        </StyledTableRow>
      </TableHead>
    </Table>
  );
};

export default QuickStandingsTable;