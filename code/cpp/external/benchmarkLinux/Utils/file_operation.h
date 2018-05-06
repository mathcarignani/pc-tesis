#ifndef FILE_OPERATION_H
#define FILE_OPERATION_H

//#include <windows.h>
#include <string.h>
#include <assert.h>
#include <sys/stat.h>
#include <sys/types.h>

static void CreateDir(char* directory)
{
	//LPSECURITY_ATTRIBUTES lpSercurity_Attributes = NULL;
	//CreateDirectory(directory,NULL);
    mode_t process_mask = umask(0);
    int result_code = mkdir(directory, 0777);
    umask(process_mask);
}

//read max 10 files
static char* GetFileName(char* input)
{
	char* temp;
	char* temp1;
	char* output = new char[200];
	::memset(output, 0, sizeof(char) * 200);
	temp = (char*) memchr (input, '/', strlen(input));

	if(temp != NULL)
		temp1 = strrchr(input,'/');

	temp = (char*) memchr (temp1, '\\', strlen(temp1));

	if(temp != NULL)
		temp1 = strrchr(temp1,'\\');

	strncpy(output, temp1 + 1, strlen(temp1) -1);

	delete[] temp;
	return output;
}

static char** ReadDir(char* directory,int& fileCount)
{
	char** files = new char*[200];
	DIR* dp;
	struct dirent *dirp;
	struct stat filestat;
	int count = 0;

    //printf(directory);
	dp = opendir(directory);
	if(dp == NULL)
	{
		printf("-----------------------Error----------------------------\n");
		printf("Read from directory fail \n");
		printf("---------------------------------------------------------------------\n");
        return NULL;
	}

	while ((dirp = readdir( dp ))&& count < 70)
	{
		char* temp = new char[200];
		::memset(temp,0,sizeof(char)*200);
		strcat(temp,directory);
		strcat(temp,"/");
		strcat(temp,dirp->d_name);

		//If the file is a directory (or is in some way invalid) we'll skip it
		if (stat(temp, &filestat ))
		{
			delete[] temp;
			continue;
		}
        //printf("%d\n", strlen(temp));
		//hard code here, S_IFDIR flag
		//if(16895 == filestat.st_mode)
        int len = strlen(temp);
        if (len < 4) {
            delete[] temp;
            continue;
        }
        char ext[3];
        strcpy(ext, temp+len-3);
        //printf("%s\n",ext);
        if (strcmp(ext,"csv") != 0)
        //if (16893 == filestat.st_mode)
		{
			delete[] temp;
			continue;
		}

		files[count++] = temp;
        //printf("%s\n",temp);
	}
    //printf("%d\n",S_IFREG);
	fileCount = count;
	closedir( dp );
	return files;
}

#endif
