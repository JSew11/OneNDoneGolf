import { useEffect, useState } from 'react';
import { useTheme } from '@mui/material';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import CircularProgress from '@mui/material/CircularProgress';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

import TournamentSeasonsApi from '../../api/tournamentSeason';
import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const TournamentStandingsTable = ({ seasonId }) => {
  const theme = useTheme();

  const [seasonTournaments, setSeasonTournaments] = useState([]);
  const [selectedTournament, setSelectedTournament] = useState(null);

  useEffect(() => {
    if (seasonId) {
      TournamentSeasonsApi.list(seasonId).then(
        (response) => {
          if (response.data.length > 0) {
            setSeasonTournaments(response.data);
            // TODO - change this once tournament api is fixed
            setSelectedTournament(response.data[0].tournament);
          }
        },
        (error) => error
      )
    }
  }, [seasonId])

  useEffect(() => {
    // TODO - get details for the selected tournament's field
  }, [selectedTournament]);

  const handleChange = (event)=> {
    setSelectedTournament(event.target.value);
  }

  return (
    <Table stickyHeader size='small' className='py-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan='4'>
            {
              selectedTournament ?
                <FormControl fullWidth>
                  <InputLabel
                    id='tournament-select-label'
                    sx={{
                      color: theme.palette.primary.contrastText,
                      '&.Mui-focused': {
                        color: theme.palette.primary.contrastText
                      }
                    }}
                  >Tournament</InputLabel>
                  <Select
                    labelId='tournament-select-label'
                    id='tournament-select'
                    value={selectedTournament}
                    label='Tournament'
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
                      seasonTournaments.map((tournament) => (
                        // TODO - refine this once tournament api is fixed
                        <MenuItem value={tournament.tournament}>
                          SAMPLE
                        </MenuItem>
                      ))
                    }
                  </Select>
                </FormControl>
              :
                'Loading Tournament Data'
            }
          </StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Place</StyledTableCell>
          <StyledTableCell align='center'>Prize Money</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && seasonTournaments.length > 0 ?
          // render table data
          <StyledTableRow key={0}>
            <StyledTableCell>SAMPLE</StyledTableCell>
            <StyledTableCell align='center'>SAMPLE</StyledTableCell>
            <StyledTableCell align='center'>SAMPLE</StyledTableCell>
          </StyledTableRow>
            :
          // loading circle
          <StyledTableRow>
            <StyledTableCell align='center' colSpan='4'>
              <CircularProgress className='my-4' size='50px'/>
            </StyledTableCell>
          </StyledTableRow>
        }
      </TableBody>
    </Table>
  )
}

export default TournamentStandingsTable;