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

import SeasonTournamentsApi from '../../api/seasonTournament';
import SeasonTournamentGolfersApi from '../../api/seasonTournamentGolfers';
import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTableCell,
  StyledTitleCell
} from 'src/assets/components/styledTable/tableCells';

const TournamentStandingsTable = ({ seasonId }) => {
  const theme = useTheme();

  const [seasonTournaments, setSeasonTournaments] = useState([]);
  const [selectedTournament, setSelectedTournament] = useState(null);
  const [selectedTournamentGolfers, setSelectedTournamentGolfers] = useState([]);

  useEffect(() => {
    if (seasonId) {
      SeasonTournamentsApi.list(seasonId).then(
        (response) => {
          if (response.data.length > 0) {
            setSeasonTournaments(response.data);
            setSelectedTournament(response.data[0].tournament);
          }
        },
        (error) => error
      )
    }
  }, [seasonId])

  useEffect(() => {
    if (seasonId && selectedTournament.id) {
      SeasonTournamentGolfersApi.list(seasonId, selectedTournament.id).then(
        (response) => {
          if (response.data.length > 0) {
            setSelectedTournamentGolfers(response.data.sort((a,b) => {
              return a.position - b.position;
            }));
          }
        }
      )
    }
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
                  >
                    Tournament
                  </InputLabel>
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
                      seasonTournaments.map((seasonTournament) => (
                        <MenuItem key={seasonTournament.tournament.id} value={seasonTournament.tournament}>
                          {seasonTournament.tournament.name}
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
          <StyledTableCell align='center'>Place</StyledTableCell>
          <StyledTableCell>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Prize Money</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && seasonTournaments.length > 0 ?
          // render table data
            selectedTournamentGolfers.map((tournamentGolfer) => (
              <StyledTableRow key={tournamentGolfer.id}>
                <StyledTableCell align='center'>
                  {tournamentGolfer.position}
                </StyledTableCell>
                <StyledTableCell>
                  {tournamentGolfer.golfer_season.golfer.first_name} {tournamentGolfer.golfer_season.golfer.last_name}
                </StyledTableCell>
                <StyledTableCell align='center'>
                  {'$' + Number(tournamentGolfer.prize_money).toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')}
                </StyledTableCell>
              </StyledTableRow>
            ))
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