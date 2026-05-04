import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import CircularProgress from '@mui/material/CircularProgress';
import { responsiveFontSizes, styled } from '@mui/material/styles';
import { useTheme } from '@mui/material';

import SeasonsApi from 'src/api/season';
import SeasonTournamentsApi from 'src/api/seasonTournament';
import SeasonTournamentGolfersApi from 'src/api/seasonTournamentGolfer';
import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';

const FullTournamentTable = ({ seasonId }) => {
  const theme = useTheme();

  const [seasonTournaments, setSeasonTournaments] = useState([]);
  const [selectedTournamentId, setSelectedTournamentId] = useState(null);
  const [allTournamentGolfers, setAllTournamentGolfers] = useState([]);
  const [pickedTournamentGolfers, setPickedTournamentGolfers] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [onlyShowPicked, setOnlyShowPicked] = useState(false);

  useEffect(() => {
    if (seasonId) {
      SeasonTournamentsApi.list(seasonId).then(
        (response) => {
          if (response.status === 200) {
            const availableTournaments = response.data.filter((tournament) => {
              return Date.parse(tournament.start_date) < Date.now();
            });
            setSeasonTournaments(availableTournaments);
            setSelectedTournamentId(availableTournaments[0].tournament.id);
          }
        },
        (error) => error
      );
      SeasonsApi.activeTournament(seasonId).then(
        (response) => {
          if (response.status === 200) {
            setSelectedTournamentId(response.data.id);
          }
        }
      )
    }
  }, [seasonId]);

  useEffect(() => {
    if (seasonId && selectedTournamentId) {
      SeasonTournamentGolfersApi.list(seasonId, selectedTournamentId).then(
        (response) => {
          if (response.data.length > 0) {
            const allGolfersData = response.data
            .sort((a,b) => {
              console.log(a.position, b.position);
              if (a.position === null) return 999999 - b.position;
              if (b.position === null) return a.position - 999999;
              return a.position - b.position;
            })
            setAllTournamentGolfers(allGolfersData);
            const pickedGolfersData = allGolfersData.filter((golfer) => golfer.picked ?? false);
            setPickedTournamentGolfers(pickedGolfersData);
            if (onlyShowPicked) {
              setTableData(pickedGolfersData);
            } else {
              setTableData(allGolfersData);
            }
          }
        }
      )
    }
  }, [seasonId, selectedTournamentId]);

  useEffect(() => {
    if (onlyShowPicked) {
      setTableData(pickedTournamentGolfers);
    } else {
      setTableData(allTournamentGolfers);
    }
  }, [onlyShowPicked])

  const handleChange = (event)=> {
    setSelectedTournamentId(event.target.value);
  }

  const handleHideUnpickedGolfersChange = () => {
    setOnlyShowPicked(!onlyShowPicked);
  }

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={11}>
            {
              selectedTournamentId && seasonTournaments.length > 0 ?
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
                    value={selectedTournamentId}
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
                        <MenuItem key={seasonTournament.tournament.id} value={seasonTournament.tournament.id}>
                          {seasonTournament.tournament.name}
                        </MenuItem>
                      ))
                    }
                  </Select>
                </FormControl>
              :
                'Loading Table Data'
            }
          </StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='filters'>
          <StyledTableCell colSpan={11} sx={{ borderBottom: 0 }}>
            <Checkbox
              className='py-0 my-0'
              checked={onlyShowPicked}
              onChange={handleHideUnpickedGolfersChange}
              inputProps={{ 'aria-label': 'controlled' }}
            /> Hide Unpicked Golfers
          </StyledTableCell>
        </StyledTableRow>
        <StyledTableRow key='header'>
          <StyledTableCell align='right'>Place</StyledTableCell>
          <StyledTableCell>Golfer</StyledTableCell>
          <StyledTableCell align='center'>Overall</StyledTableCell>
          <StyledTableCell align='center'>Today</StyledTableCell>
          <StyledTableCell>Thru</StyledTableCell>
          <StyledTableCell>R1</StyledTableCell>
          <StyledTableCell>R2</StyledTableCell>
          <StyledTableCell>R3</StyledTableCell>
          <StyledTableCell>R4</StyledTableCell>
          <StyledTableCell>Total</StyledTableCell>
          <StyledTableCell>Winnings</StyledTableCell>
        </StyledTableRow>
      </TableHead>
      <TableBody>
        {
          seasonId && selectedTournamentId && tableData.length > 0 ?
          // render table data
            tableData.map((tournamentGolfer) => (
              <TournamentTableRow key={tournamentGolfer.id} golferPicked={tournamentGolfer.picked ?? false} onlyPicked={onlyShowPicked}>
                <StyledTableCell align='right'>
                  {tournamentGolfer.position}
                </StyledTableCell>
                <StyledTableCell>
                  {tournamentGolfer.golfer_season.golfer.first_name} {tournamentGolfer.golfer_season.golfer.last_name}
                </StyledTableCell>
                <StyledTableCell align='center'>
                  N/A {/* TODO - Overall */}
                </StyledTableCell>
                <StyledTableCell align = 'center'>
                  N/A {/* TODO - Today */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - Thru */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - R1 */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - R2 */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - R3 */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - R4 */}
                </StyledTableCell>
                <StyledTableCell>
                  N/A {/* TODO - Total */}
                </StyledTableCell>
                <StyledTableCell>
                  {'$' + Number(tournamentGolfer.prize_money).toFixed(0).replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')}
                </StyledTableCell>
              </TournamentTableRow>
            ))
          :
            <StyledTableRow>
              <StyledTableCell align='center' colSpan={11}>
                <CircularProgress className='my-4' size='50px'/>
              </StyledTableCell>
            </StyledTableRow>
        }
      </TableBody>
    </Table>
  );
}

const TournamentTableRow = styled(StyledTableRow, {
  shouldForwardProp: (prop) => prop !== 'golferPicked' && prop !== 'onlyPicked'
}) (({ theme, golferPicked, onlyPicked }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: (golferPicked && !onlyPicked ? theme.palette.picked.light : theme.palette.action.light),
  },
  '&:nth-of-type(even)': {
    backgroundColor: (golferPicked && !onlyPicked ? theme.palette.picked.dark : theme.palette.action.hover),
  },
}));

export default FullTournamentTable;