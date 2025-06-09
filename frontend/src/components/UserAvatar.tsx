import { Avatar, Box } from '@mui/material';
import { Person as PersonIcon } from '@mui/icons-material';

interface UserAvatarProps {
  name: string;
  avatarUrl?: string;
  size?: 'small' | 'medium' | 'large';
}

function UserAvatar({ name, avatarUrl, size = 'large' }: UserAvatarProps) {
  const generateAvatarUrl = (name: string) => {
    const seed = encodeURIComponent(name.toLowerCase().replace(/\s+/g, ''));
    return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}&backgroundColor=b6e3f4,c0aede,d1d4f9`;
  };

  const finalAvatarUrl = avatarUrl || generateAvatarUrl(name);

  const sizeStyles = {
    small: { width: 40, height: 40, fontSize: 16 },
    medium: { width: 80, height: 80, fontSize: 32 },
    large: { width: 120, height: 120, fontSize: 48 },
  };

  const currentSize = sizeStyles[size];

  return (
    <Box display="flex" justifyContent="center">
      <Avatar
        src={finalAvatarUrl}
        alt={`${name}'s avatar`}
        sx={{
          width: currentSize.width,
          height: currentSize.height,
          fontSize: currentSize.fontSize,
          fontWeight: 'bold',
          border: 4,
          borderColor: 'primary.main',
          boxShadow: 3,
        }}
      >
        {!finalAvatarUrl && (name.charAt(0).toUpperCase() || <PersonIcon />)}
      </Avatar>
    </Box>
  );
}

export default UserAvatar;
