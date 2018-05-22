#ifndef __APCAENTRY_H
#define __APCAENTRY_H

struct APCAEntry
{
public:
	double value;
	int endingTimestamp;

	APCAEntry()
	{
		value = 0;
		endingTimestamp = 0;
	};

	APCAEntry(double v, int e)
	{
		value = v;
		endingTimestamp = e;
	};
};

#endif