import { Paper, Typography, Box } from '@mui/material';
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  Legend
} from 'recharts';
import type { Skill } from '../types/user';

interface SkillsRadarChartProps {
  skills: Skill[];
}

function SkillsRadarChart({ skills }: SkillsRadarChartProps) {
  const chartData = skills.map(skill => ({
    skill: skill.name,
    level: skill.level,
    fullMark: 10,
  }));

  const colors = {
    stroke: '#8884d8',
    fill: '#8884d8',
    fillOpacity: 0.3,
  };

  return (
    <Paper elevation={3} sx={{ p: 3, height: 500 }}>
      <Typography variant="h5" component="h2" gutterBottom align="center">
        Skills Overview
      </Typography>
      
      {skills.length === 0 ? (
        <Box 
          display="flex" 
          justifyContent="center" 
          alignItems="center" 
          height="400px"
        >
          <Typography variant="body1" color="text.secondary">
            No skills data available
          </Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={chartData} margin={{ top: 20, right: 80, bottom: 20, left: 80 }}>
            <PolarGrid />
            <PolarAngleAxis 
              dataKey="skill" 
              tick={{ fontSize: 12, fill: '#666' }}
            />
            <PolarRadiusAxis 
              angle={0} 
              domain={[0, 10]} 
              tick={{ fontSize: 10, fill: '#666' }}
              tickCount={6}
            />
            <Radar
              name="Skill Level"
              dataKey="level"
              stroke={colors.stroke}
              fill={colors.fill}
              fillOpacity={colors.fillOpacity}
              strokeWidth={2}
            />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      )}
      
      <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 2 }}>
        Skills are rated from 1 to 10 based on proficiency level
      </Typography>
    </Paper>
  );
}

export default SkillsRadarChart;
