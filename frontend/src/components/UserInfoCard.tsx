import { 
  Paper, 
  Typography, 
  Box, 
  Chip,
  Stack,
  Divider 
} from '@mui/material';
import { 
  Work as WorkIcon,
  Email as EmailIcon,
  CalendarToday as CalendarIcon 
} from '@mui/icons-material';
import UserAvatar from './UserAvatar';
import type { User, Skill } from '../types/user';

interface UserInfoCardProps {
  user: User;
  skills: Skill[];
}

function UserInfoCard({ user, skills }: UserInfoCardProps) {
  const skillsByCategory = skills.reduce((acc, skill) => {
    if (!acc[skill.category]) {
      acc[skill.category] = [];
    }
    acc[skill.category].push(skill);
    return acc;
  }, {} as Record<string, Skill[]>);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Box display="flex" flexDirection="column" alignItems="center" mb={3}>
        <UserAvatar name={user.name} avatarUrl={user.avatar_url} />
        
        <Typography variant="h4" component="h1" mt={2} gutterBottom>
          {user.name}
        </Typography>
        
        <Typography variant="h6" color="primary" gutterBottom>
          {user.position}
        </Typography>
      </Box>

      <Divider sx={{ mb: 3 }} />

      <Stack spacing={2}>
        <Box display="flex" alignItems="center" gap={2}>
          <EmailIcon color="action" />
          <Typography variant="body1">{user.email}</Typography>
        </Box>

        <Box display="flex" alignItems="center" gap={2}>
          <CalendarIcon color="action" />
          <Typography variant="body1">
            Member since {formatDate(user.created_at)}
          </Typography>
        </Box>

        <Box mt={3}>
          <Typography variant="h6" gutterBottom display="flex" alignItems="center" gap={1}>
            <WorkIcon />
            Skills Summary
          </Typography>
          
          <Typography variant="body2" color="text.secondary" mb={2}>
            Total Skills: {skills.length}
          </Typography>

          {Object.keys(skillsByCategory).length > 0 && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Categories:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                {Object.entries(skillsByCategory).map(([category, categorySkills]) => (
                  <Chip
                    key={category}
                    label={`${category} (${categorySkills.length})`}
                    variant="outlined"
                    size="small"
                    color="primary"
                  />
                ))}
              </Stack>
            </Box>
          )}
        </Box>

        {skills.length > 0 && (
          <Box mt={2}>
            <Typography variant="subtitle2" gutterBottom>
              Top Skills:
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              {skills
                .sort((a, b) => b.level - a.level)
                .slice(0, 5)
                .map((skill) => (
                  <Chip
                    key={skill.id}
                    label={`${skill.name} (${skill.level}/10)`}
                    color="secondary"
                    size="small"
                  />
                ))}
            </Stack>
          </Box>
        )}
      </Stack>
    </Paper>
  );
}

export default UserInfoCard;
