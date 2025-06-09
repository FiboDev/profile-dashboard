import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Box, 
  Alert, 
  CircularProgress, 
  Typography,
  Button
} from '@mui/material';
import { Logout as LogoutIcon } from '@mui/icons-material';
import UserInfoCard from '../components/UserInfoCard';
import SkillsRadarChart from '../components/SkillsRadarChart';
import type { User, Skill } from '../types/user';
import { UserService, SkillService } from '../services/user';
import AuthService from '../services/auth';
import { ApiError } from '../services/api';

interface ProfilePageProps {
  userId?: number;
}

function ProfilePage({ userId: propUserId }: ProfilePageProps) {
  const { userId: paramUserId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const effectiveUserId = propUserId || parseInt(paramUserId || '1', 10);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setLoading(true);
        setError(null);

        // Try to get user profile with skills from FastAPI backend
        try {
          const userProfile = await UserService.getUserProfile(effectiveUserId);
          setUser(userProfile);
          setSkills(userProfile.skills || []);
        } catch (profileError) {
          // If profile endpoint fails, try individual endpoints
          console.warn('Profile endpoint failed, trying individual endpoints:', profileError);
          
          const [userResponse, skillsResponse] = await Promise.all([
            UserService.getUserById(effectiveUserId),
            SkillService.getUserSkills(effectiveUserId)
          ]);
          
          setUser(userResponse);
          setSkills(skillsResponse);
        }

      } catch (err) {
        console.error('Error fetching user profile:', err);
        
        if (err instanceof ApiError) {
          if (err.status === 401) {
            setError('You are not authorized to view this profile. Please log in.');
            // Redirect to login after a delay
            setTimeout(() => navigate('/login'), 2000);
          } else if (err.status === 403) {
            setError('You can only view your own profile.');
          } else if (err.status === 404) {
            setError('User not found.');
          } else if (err.status === 0) {
            setError('Unable to connect to server. Please check your connection.');
          } else {
            setError(`Error loading profile: ${err.message}`);
          }
        } else {
          setError('Failed to load user profile. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [effectiveUserId, navigate]);

  const handleLogout = async () => {
    try {
      await AuthService.logout();
      navigate('/login');
    } catch (err) {
      console.error('Logout error:', err);
      // Even if logout fails, redirect to login
      navigate('/login');
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
          <CircularProgress size={60} />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  if (!user) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="warning" sx={{ mb: 3 }}>
          User not found.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header with logout button */}
      <Box 
        display="flex" 
        justifyContent="space-between" 
        alignItems="center" 
        mb={4}
        sx={{ 
          borderBottom: 1, 
          borderColor: 'divider', 
          pb: 2 
        }}
      >
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Profile Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Employee Information & Skills Overview
          </Typography>
        </Box>
        <Button
          variant="outlined"
          color="primary"
          startIcon={<LogoutIcon />}
          onClick={handleLogout}
          sx={{ minWidth: 100 }}
        >
          Logout
        </Button>
      </Box>

      <Box 
        display="flex" 
        flexDirection={{ xs: 'column', md: 'row' }} 
        gap={4}
      >
        {/* User Information Card */}
        <Box flex={{ xs: '1', md: '0 0 33%' }}>
          <UserInfoCard user={user} skills={skills} />
        </Box>

        {/* Skills Radar Chart */}
        <Box flex={{ xs: '1', md: '1' }}>
          <SkillsRadarChart skills={skills} />
        </Box>
      </Box>
    </Container>
  );
}

export default ProfilePage;
