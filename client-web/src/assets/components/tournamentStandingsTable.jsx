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

const TournamentStandingsTable = ({ seasonId }) => {
  const [seasonTournaments, setSeasonTournaments] = useState([]);

  useEffect(() => {
    // TODO - get a list of all tournaments in the season so they can be selected from a dropdown
  }, [seasonId])

  return (
    <Table stickyHeader size='small' className='py-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan='4'>TODO - Tournament Selector Dropdown</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='center'>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Place</StyledTableCell>
          <StyledTableCell align='center'>Prize Money</StyledTableCell>
        </StyledTableRow>
      </TableHead>
    </Table>
  )
}

export default TournamentStandingsTable;