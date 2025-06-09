import { Container, Box } from '@mui/material';
import LoginForm from '../components/LoginForm';

function Login() {
  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
        sx={{ py: 4 }}
      >
        <LoginForm />
      </Box>
    </Container>
  );
}

export default Login;