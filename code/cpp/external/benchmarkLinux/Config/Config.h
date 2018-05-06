#ifndef __CONFIG_H
#define __CONFIG_H

#include "../stdafx.h"
//#include "windows.h"
#include "string.h"
#include "time.h"
class Config
{
public:
	static char * pfile;
	static char * rfile;
	static int getInt(char * sName, char * pName)
	{
		//int i = GetPrivateProfileInt(sName,pName, -1, pfile);
        dictionary * ini = iniparser_load(pfile);
        //iniparser_dump(ini, stderr);
        char * tmp = new char[100];
        strcpy(tmp,sName);
        strcat(tmp,":");
        strcat(tmp,pName);
        int i = iniparser_getint(ini,tmp, -1);
        //iniparser_freedict(ini);
		if(i < 0)
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Miss %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}
		return i;
	}

	static float getDouble(char * sName, char * pName)
	{
        dictionary * ini = iniparser_load(pfile);
        //iniparser_dump(ini, stderr);
        char * tmp = new char[100];
        strcpy(tmp,sName);
        strcat(tmp,":");
        strcat(tmp,pName);
        double d = iniparser_getdouble(ini,tmp, -1.0);
        //iniparser_freedict(ini);
		if(d < 0.0)
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Miss %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}
		return d;
		/*char * buffer = new char[100];
		GetPrivateProfileString(sName, pName, NULL, buffer, 100, pfile);
		if(!strcmp(buffer,""))
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Miss %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}
		float pValue = atof(buffer);
		if(pValue<0)
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Error value %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}
		delete [] buffer;
		return pValue;*/
	}

	static void getString(char * sName, char * pName, char * pValue)
	{
        dictionary * ini = iniparser_load(pfile);
        //iniparser_dump(ini, stderr);
        char tmp[100];
        strcpy(tmp,sName);
        strcat(tmp,":");
        strcat(tmp,pName);
        char* s = iniparser_getstring(ini,tmp, NULL);
        strcpy(pValue,s);
        //iniparser_freedict(ini);
		if(pValue == NULL)
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Miss %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}
        //printf(pValue);
        //printf("\n");
		/*GetPrivateProfileString(sName, pName, NULL, pValue, 300, pfile);
		if(!strcmp(pValue,""))
		{
			printf("-----------------------Miss Configuration----------------------------\n");
			printf("Miss %s of %s in config.ini.\n", pName, sName);
			printf("---------------------------------------------------------------------\n");
			exit(-1);
		}*/
	}

	static void writeDouble(char * sName, char * pName, float pValue)
	{
		char * buffer = new char[100];
		sprintf(buffer, " %f", pValue);
        dictionary * ini = iniparser_load(pfile);
        //iniparser_dump(ini, stderr);
        char * tmp = new char[100];
        strcpy(tmp,sName);
        strcat(tmp,":");
        strcat(tmp,pName);
        iniparser_getstring(ini,tmp,buffer);
        //iniparser_freedict(ini);

		//WritePrivateProfileString(sName, pName, buffer, rfile);
		//delete [] buffer;
	}

	// Add ----> A
	static void FreeMemoryForClass()
	{
		if(pfile != NULL)
		{
			delete []pfile;
		}
		if(rfile != NULL)
		{
			delete[]rfile;
		}
	}
	// Add <---- A
};

#endif
