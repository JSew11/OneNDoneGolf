import { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import Checkbox from '@mui/material/Checkbox';
import CircularProgress from '@mui/material/CircularProgress';
import { styled } from '@mui/material/styles';
import { useTheme } from '@mui/material';

import StyledTableRow from 'src/assets/components/styledTable/row';
import {
  StyledTitleCell,
  StyledTableCell
} from 'src/assets/components/styledTable/tableCells';
import SeasonTournamentGolferApi from 'src/api/seasonTournamentGolfer';

const FullTournamentTable = ({ season, tournament }) => {
  const theme = useTheme();

  const [allTournamentGolfers, setAllTournamentGolfers] = useState([]);
  const [pickedTournamentGolfers, setPickedTournamentGolfers] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [onlyShowPicked, setOnlyShowPicked] = useState(false);

  useEffect(() => {
    if (season && tournament) {
      SeasonTournamentGolferApi.list(season.id, tournament.id).then(
        (response) => {
          if (response.data.length > 0) {
            const initialData = response.data.sort((a,b) => {
              return a.position - b.position;
            })
            setAllTournamentGolfers(initialData);
            setPickedTournamentGolfers(initialData.filter((golfer) => golfer.picked ?? false));
            setTableData(initialData);
          }
        }
      )
    }
  }, []);

  useEffect(() => {
    if (onlyShowPicked) {
      setTableData(pickedTournamentGolfers);
    } else {
      setTableData(allTournamentGolfers);
    }
  }, [onlyShowPicked])

  const handleCheckboxChange = () => {
    setOnlyShowPicked(!onlyShowPicked);
  }

  return (
    <Table stickyHeader size='small' className='my-0 pb-3'>
      <TableHead>
        <StyledTableRow key='title'>
          <StyledTitleCell colSpan={11}>{
            season && tournament ? 
              tournament.name
            :
              'Loading Active Tournament'
          }</StyledTitleCell>
        </StyledTableRow>
        <StyledTableRow key='filters'>
          <StyledTableCell colSpan={11} sx={{ borderBottom: 0 }}>
            <Checkbox
              className='py-0 my-0'
              checked={onlyShowPicked}
              onChange={handleCheckboxChange}
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
          season && tournament && tableData.length > 0 ?
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
          // loading circle
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