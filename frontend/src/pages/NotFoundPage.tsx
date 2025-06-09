import { Box, Typography, Button, Container, Paper } from '@mui/material';
import { Home as HomeIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

function NotFoundPage() {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 6, textAlign: 'center' }}>
        <Box mb={4}>
          <Typography 
            variant="h1" 
            component="h1" 
            sx={{ 
              fontSize: '8rem', 
              fontWeight: 'bold', 
              color: 'primary.main',
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
            }}
          >
            404
          </Typography>
        </Box>

        <Typography variant="h4" component="h2" gutterBottom color="text.primary">
          Oops! Page Not Found
        </Typography>

        <Typography variant="body1" color="text.secondary" paragraph sx={{ mb: 4 }}>
          The page you're looking for doesn't exist or has been moved.
          Let's get you back on track!
        </Typography>

        <Box 
          display="flex" 
          flexDirection={{ xs: 'column', sm: 'row' }} 
          gap={2} 
          justifyContent="center"
          alignItems="center"
        >
          <Button
            variant="contained"
            color="primary"
            size="large"
            startIcon={<HomeIcon />}
            onClick={handleGoHome}
            sx={{ minWidth: 150 }}
          >
            Go Home
          </Button>

          <Button
            variant="outlined"
            color="primary"
            size="large"
            startIcon={<ArrowBackIcon />}
            onClick={handleGoBack}
            sx={{ minWidth: 150 }}
          >
            Go Back
          </Button>
        </Box>

        <Box mt={6}>
          <Typography variant="body2" color="text.secondary">
            If you think this is an error, please contact our support team.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default NotFoundPage;
