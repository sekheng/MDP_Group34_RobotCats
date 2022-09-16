package com.example.robotcatmobile.home_parts;

import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipDescription;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Typeface;
import android.os.Build;
import android.view.DragEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.widget.AppCompatButton;
import androidx.appcompat.widget.AppCompatImageView;
import androidx.core.content.ContextCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.HomeFrag;
import com.example.robotcatmobile.R;
import com.example.robotcatmobile.bluetooth_parts.BluetoothConn;

import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/**
responsible for creating the grid and everything else that should part of it
 */
@RequiresApi(api = Build.VERSION_CODES.N)
public class GridRecycler extends RecyclerView.Adapter<GridRecycler.ViewHolder> {
    /**
     * To help with converting enum to string
     * @param
     * @return array of enums in string
     */
    public static String[] getNames(Class<? extends Enum<?>> e) {
        return Arrays.stream(e.getEnumConstants()).map(Enum::name).toArray(String[]::new);
    }

    public static final String DIRECTION_KEY = "direction";
    public static final String SYMBOL_KEY = "symbol";
    public static final String X_KEY = "x";
    public static final String Y_KEY = "y";
    public static final String ROBOT_VALUE = "robot";
    public static final String OBSTACLE_VALUE = "obstacle";
    public static final String FONT_SIZE_KEY = "fontsize";

    public static final int COLUMNS = 15;

    public static final int ROWS = 15;

    final int mWidthOfRobot = 3;

    // unfortunate hardcoding to know whether the robot is there or not!
    public static boolean mIsRobotPlaced = false;
    // the array of grids
    public ViewHolder[] arrOfGrids = new ViewHolder[COLUMNS * ROWS];

    // then the robot image view to overlay it on top of the grid!
    AppCompatImageView mRobotImg;
    // to set the robot direction!
    // north as default!
    Direction mRobotDirection = Direction.NORTH;
    // angle of the robot. we will be assuming north is 0 degrees!
    int mAngleOfRobot = mRobotDirection.getValue();
    // the coordinate of the robot along x-axis
    int mRobotX;
    // coordinate of the robot along y-axis
    int mRobotY;
    // to know the state of the interaction with the grid
    public static SET_GRID_STATE curInteractState = SET_GRID_STATE.NONE;
    // the shadow
    View.DragShadowBuilder mMyShadow;
    // string of all possible images!
    String[] mAllObstacleSymbols = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "up","down","left","right","circle","square","V","W","X","Y","Z","E","F","G","H","S","T","U"};
    // to type being send to here
    BroadcastReceiver mTypeBR = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String jsonString = intent.getStringExtra(BluetoothConn.SENDING_TYPE);
            try {
                JSONObject json = new JSONObject(jsonString);
                String type = json.get(BluetoothConn.SENDING_TYPE).toString();
                // lots of checks to be JUST IN CASE
                if (json.has(DIRECTION_KEY) && json.has(X_KEY) && json.has(Y_KEY)) {
                    int y = json.getInt(Y_KEY);
                    int x = json.getInt(X_KEY);
                    // then look at the direction
                    Direction curDir = Direction.NONE;
                    String directionStr = json.getString(DIRECTION_KEY);
                    // iterate through enums to see if it works
                    for (Direction dir: Direction.values()) {
                        if (dir.toString().equalsIgnoreCase(directionStr)) {
                            curDir = dir;
                            break;
                        }
                    }
                    if (x < COLUMNS && y < ROWS) {
                        if (type.equalsIgnoreCase(OBSTACLE_VALUE)) {
                            // then this is an obstacle
                            String symbol = json.getString(SYMBOL_KEY);
                            // access the grid straight away
                            ViewHolder theGrid = arrOfGrids[x + (y * ROWS)];
                            theGrid.setObstacle(true);
                            theGrid.setObstacleImage(symbol);
                            theGrid.setObstacleDirection(curDir);
                            if (json.has(FONT_SIZE_KEY)) {
                                theGrid.mGridButton.setTextSize((float)json.getInt(FONT_SIZE_KEY));
                            }
                        } else if (type.equalsIgnoreCase(ROBOT_VALUE)) {
                            placeRobot(x,y);
                            mAngleOfRobot = curDir.getValue();
                            // we can reuse and fake it
                            rotateRobot(0);
                        }
                    }
                }

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };

    // to listen to the direction of the robot
    BroadcastReceiver mDirectionBR = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String jsonString = intent.getStringExtra(HomeFrag.ROBOT_DIRECTION);
            try {
                JSONObject json = new JSONObject(jsonString);
                String direction = json.get(HomeFrag.ROBOT_DIRECTION).toString();
                switch (direction) {
                    case HomeFrag.ROBOT_LEFT:
                        rotateRobot(-90);
                        break;
                    case HomeFrag.ROBOT_RIGHT:
                        rotateRobot(90);
                        break;
                    case HomeFrag.ROBOT_REVERSE:
                        moveRobot(false);
                        break;
                    case HomeFrag.ROBOT_UP:
                        moveRobot(true);
                        break;
                    default:
                        break;
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };

    void moveRobot(boolean isForward) {
        int moveX = 1;
        int moveY = 1;
        if (isForward) {
            moveY = -1;
            moveX = -1;
        }
        switch (mRobotDirection) {
            case WEST:
                moveY = 0;
                break;
            case EAST:
                moveX *= -1;
                moveY = 0;
                break;
            case SOUTH:
                moveX = 0;
                moveY *= -1;
                break;
            default:
                moveX = 0;
                break;
        }
        placeRobot(mRobotX + moveX, mRobotY + moveY);
    }

    void rotateRobot(int angle) {
        mAngleOfRobot = (mAngleOfRobot + angle) % 360;
        while (mAngleOfRobot < 0) {
            // because it is using
            mAngleOfRobot = (360 + mAngleOfRobot) % 360;
        }
        for (Direction dir : Direction.values()) {
            if (mAngleOfRobot == dir.getValue()) {
                mRobotDirection = dir;
                break;
            }
        }
        // and rotate the image
        mRobotImg.setRotation(mAngleOfRobot);
    }

    public GridRecycler() {
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.grid_button, parent, false);
        if (mRobotImg == null) {
            mRobotImg = parent.getRootView().findViewById(R.id.robot);
            // we just cheat here by hardcode everything here
            // register for the direction event
            IntentFilter directionIntent = new IntentFilter(HomeFrag.ROBOT_DIRECTION);
            LocalBroadcastManager.getInstance(parent.getContext()).registerReceiver(mDirectionBR, directionIntent);
            IntentFilter obstacle_typeIntent = new IntentFilter(BluetoothConn.SENDING_TYPE);
            LocalBroadcastManager.getInstance(parent.getContext()).registerReceiver(mTypeBR, obstacle_typeIntent);
        }
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        // setting up the position
        holder.mY = position / ROWS;
        holder.mX = position % COLUMNS;
        // then we can just set the array of grids as it is
        arrOfGrids[position] = holder;
    }

    @Override
    public int getItemCount() {
        return COLUMNS * ROWS;
    }

    // to set the robots
    public void placeRobot(int _x, int _y) {
        // we have to change the buttons to prevent it from going out of grid!
        if (_x >= COLUMNS - mWidthOfRobot) {
            _x = COLUMNS - mWidthOfRobot;
        }
        else if (_x <= 0) {
            _x = 0;
        }
        if (_y >= ROWS - mWidthOfRobot) {
            _y = ROWS - mWidthOfRobot;
        }
        else if (_y <= 0) {
            _y = 0;
        }
        ViewHolder decidedButton = arrOfGrids[_x + (_y * ROWS)];
        mRobotImg.setX((_x * decidedButton.mGridButton.getWidth()));
        mRobotImg.setY((_y * decidedButton.mGridButton.getHeight()));
        mRobotX = _x;
        mRobotY = _y;
        mRobotImg.setVisibility(View.VISIBLE);
        mIsRobotPlaced = true;
    }



    // because when drag action has ended, it will just call that event like 400 times!!
    static boolean hasDragEndedCall = true;
    /*
    The individual buttons at the grid
     */
    class ViewHolder extends RecyclerView.ViewHolder {
        /*
         position along the x axis
         */
        public int mX;
        /*
        position along the y axis
         */
        public int mY;
        // the button of this view holder
        AppCompatButton mGridButton;
        // a boolean flag to check whether is it an obstacle or not
        boolean mIsObstacle = false;
        // direction that the obstacle is facing
        // NONE as default
        Direction mDirection = Direction.NONE;
        // set the number which the obstacle is displaying
        AppCompatImageView mMainImage;
        // the symbol of this obstacle!
        String mObstacleSymbol = "";

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            mGridButton = itemView.findViewById(R.id.grid_button);
            mMainImage = itemView.findViewById(R.id.grid_symbol);
            mGridButton.setOnClickListener(view -> {
                switch (curInteractState) {
                    case ROBOT:
                        int x = this.mX;
                        int y = this.mY;
                        // then set the position of the robot according to the grid position
                        // usually the center of the position, we hardcoded it to 3x3 for now
                        switch (mWidthOfRobot) {
                            case 3:
                                x -= 1;
                                y -= 1;
                                break;
                            default:
                                break;
                        }
                        placeRobot(x, y);
                        // and then send a bluetooth message to say which grid location it is placed!
                        JSONObject jsonObject = new JSONObject();
                        try {
                            jsonObject.put(BluetoothConn.SENDING_TYPE,ROBOT_VALUE);
                            jsonObject.put(X_KEY,mRobotX);
                            jsonObject.put(Y_KEY,mRobotY);
                            jsonObject.put(DIRECTION_KEY,mRobotDirection);
                            BluetoothConn.write(jsonObject.toString().getBytes(StandardCharsets.UTF_8));
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        break;
                    case OBSTACLE:
                        setObstacleBluetooth(!mIsObstacle,"",Direction.NONE);
                        break;
                    case TYPE:
                        if (mIsObstacle) {
                            // then create the alert dialog to set it
                            AlertDialog.Builder alertBuilder = new AlertDialog.Builder(itemView.getContext());
                            alertBuilder.setTitle("Choose Obstacle");
                            alertBuilder.setItems(mAllObstacleSymbols, (dialogInterface, i) -> {
                                setObstacleBluetooth(mIsObstacle,mAllObstacleSymbols[i],mDirection);
                            });
                            AlertDialog dialog = alertBuilder.create();
                            dialog.show();
                        }
                        break;
                    case DIRECTION:
                        if (mIsObstacle) {
                            // create the alert dialog to set the direction
                            AlertDialog.Builder alertBuilder = new AlertDialog.Builder(itemView.getContext());
                            alertBuilder.setTitle("Choose Direction");
                            alertBuilder.setItems(getNames(Direction.class), (dialogInterface, i) -> {
                                setObstacleBluetooth(mIsObstacle,mObstacleSymbol,Direction.values()[i]);
                            });
                            AlertDialog dialog = alertBuilder.create();
                            dialog.show();
                        }
                        break;
                    default:
                        break;
                }
            });
            mGridButton.setOnDragListener(gridButtonDragListener);
        }

        // to listen to drag event
        View.OnDragListener gridButtonDragListener = (view, dragEvent) -> {
            if (curInteractState == SET_GRID_STATE.NONE) {
                // return true if it is handled successfully
                switch (dragEvent.getAction()) {
                    case DragEvent.ACTION_DRAG_STARTED:
                        // Determines if this View can accept the dragged data.
                        if (dragEvent.getClipDescription().hasMimeType(ClipDescription.MIMETYPE_TEXT_PLAIN)) {
                            // Returns true to indicate that the View can accept the dragged data.
                            return true;
                        }
                        // Returns false to indicate that, during the current drag and drop operation,
                        // this View will not receive events again until ACTION_DRAG_ENDED is sent.
                        return false;
                    case DragEvent.ACTION_DROP: {
                        // then set the current one as obstacle
                        ViewHolder origin = (ViewHolder) dragEvent.getLocalState();
                        setObstacleBluetooth(true, origin.mObstacleSymbol,origin.mDirection);
                        // Returns true; the value is ignored.
                        return true;
                    }
                    case DragEvent.ACTION_DRAG_ENDED: {
                        // remove the original obstacle
                        if (hasDragEndedCall) {
                            ViewHolder origin = (ViewHolder) dragEvent.getLocalState();
                            // then the origin set to be false
                            origin.setObstacleBluetooth(hasDragEndedCall = false, "", Direction.NONE);
                        }
                        return true;
                    }
                    // An unknown action type was received.
                    default:
                        break;
                }
                return true;
            }
            return false;
        };

        // to listen for long click event, only meant for obstacles!
        View.OnLongClickListener mOnLongClickListener = v -> {
            // check whether it is from this class viewholder
            if (mIsObstacle && curInteractState == SET_GRID_STATE.NONE)
            {
                // Create a new ClipData.
                // This is done in two steps to provide clarity. The convenience method
                // ClipData.newPlainText() can create a plain text ClipData in one step.
                JSONObject buttonObj = new JSONObject();
                try {
                    buttonObj.put("x",mX);
                    buttonObj.put("y",mY);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                // Create a new ClipData.Item from the ImageView object's tag.
                ClipData.Item item = new ClipData.Item(buttonObj.toString());
                // Create a new ClipData using the tag as a label, the plain text MIME type, and
                // the already-created item. This creates a new ClipDescription object within the
                // ClipData and sets its MIME type to "text/plain".
                ClipData dragData = new ClipData(
                        buttonObj.toString(),
                        new String[]{ClipDescription.MIMETYPE_TEXT_PLAIN},
                        item);
                // Instantiate the drag shadow builder.
                mMyShadow = new View.DragShadowBuilder(v);
                // Start the drag.
                v.startDragAndDrop(dragData,  // The data to be dragged
                        mMyShadow,  // The drag shadow builder
                        this,
                        0          // Flags (not currently used, set to 0)
                );
                // Indicate that the long-click was handled.
                return hasDragEndedCall = true;
            }
            return false;
        };

        // the direction that the obstacle is facing
        public void setObstacleDirection(Direction direction) {
            AppCompatImageView theBorder = getBorderView(direction);
            // then we have to change the color accordingly!
            AppCompatImageView previousBorder = getBorderView(mDirection);
            if (previousBorder != null) {
                previousBorder.setVisibility(View.INVISIBLE);
            }
            if (direction != Direction.NONE) {
                theBorder.setVisibility(View.VISIBLE);
            }
            mDirection = direction;
        }

        // the border view
        AppCompatImageView getBorderView(Direction direction) {
            View parentView = (View)mGridButton.getParent();
            switch (direction) {
                case NORTH:
                    return parentView.findViewById(R.id.grid_top_border);
                case EAST:
                    return parentView.findViewById(R.id.grid_right_border);
                case WEST:
                    return parentView.findViewById(R.id.grid_left_border);
                case SOUTH:
                    return parentView.findViewById(R.id.grid_bottom_border);
                default:
                    return null;
            }
        }

        // the obstacle to be set!
        public void setObstacleImage(String obstacleLook) {
            mGridButton.setText("");
            mMainImage.setVisibility(View.VISIBLE);
            //"up","down","left","right","circle","square"
            // we will need to know whether it is a circle or not
            // HARDCODE
            if (obstacleLook.equalsIgnoreCase("circle")) {
                // make sure the text is empty
                mMainImage.setImageResource(R.drawable.circle);
            }
            else if (obstacleLook.equalsIgnoreCase("up")) {
                mMainImage.setImageResource(R.drawable.up_arrow);
            }
            else if (obstacleLook.equalsIgnoreCase("down")) {
                mMainImage.setImageResource(R.drawable.down_arrow);
            }
            else if (obstacleLook.equalsIgnoreCase("left")) {
                mMainImage.setImageResource(R.drawable.left_arrow);
            }
            else if (obstacleLook.equalsIgnoreCase("right")) {
                mMainImage.setImageResource(R.drawable.right_arrow);
            }
            else if (obstacleLook.equalsIgnoreCase("square")) {
                mMainImage.setImageResource(R.drawable.square_square);
            }
            else
            {
                mMainImage.setVisibility(View.INVISIBLE);
                mGridButton.setText(obstacleLook);
            }
            mObstacleSymbol = obstacleLook;
            mGridButton.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
        }

        void setObstacleBluetooth(boolean isObstacle,
                                  String imageStr,
                                  Direction direction) {
            // just for the grid button to send the obstacle over
            JSONObject jsonObject = new JSONObject();
            try {
                jsonObject.put(BluetoothConn.SENDING_TYPE,OBSTACLE_VALUE);
                jsonObject.put(X_KEY,mX);
                jsonObject.put(Y_KEY,mY);
                jsonObject.put(SYMBOL_KEY, imageStr);
                jsonObject.put(DIRECTION_KEY, direction.toString());
                BluetoothConn.write(jsonObject.toString().getBytes(StandardCharsets.UTF_8));
            } catch (JSONException e) {
                e.printStackTrace();
            }
            setObstacle(isObstacle);
            setObstacleImage(imageStr);
            setObstacleDirection(direction);
        }

        public void setObstacle(boolean isObstacle) {
            mIsObstacle = isObstacle;
            // then change the button accordingly!
            // just by marking the button black to stand as obstacle
            if (mIsObstacle) {
                mGridButton.setBackground(ContextCompat.getDrawable(mGridButton.getContext(), R.drawable.obstacle_design));
                mGridButton.setOnLongClickListener(mOnLongClickListener);
            }
                // we can also toggle between clear space and obstacle!
            else {
                mGridButton.setBackground(ContextCompat.getDrawable(mGridButton.getContext(), R.drawable.grid_design));
                mGridButton.setOnLongClickListener(null);
                setObstacleDirection(Direction.NONE);
                setObstacleImage("");
            }
        }
    }
}
